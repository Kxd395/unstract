from typing import Optional

from account.models import User
from api.models import APIDeployment
from api.notification import APINotification
from workflow_manager.workflow.models.execution import WorkflowExecution


class APIDeploymentUtils:
    @staticmethod
    def get_api_by_id(
        api_id: str, user: Optional[User] = None
    ) -> Optional[APIDeployment]:
        """Retrieves an APIDeployment instance by its unique ID.

        Args:
            api_id (str): The unique identifier of the APIDeployment to retrieve.
            user (Optional[User]): The user who must have created the APIDeployment.
                If provided, only return the deployment if it was created by this user.
                else return the deployment with the given ID.

        Returns:
            Optional[APIDeployment]: The APIDeployment instance if found,
                otherwise None.
        """
        try:
            if user:
                api_deployment: APIDeployment = APIDeployment.objects.get(
                    pk=api_id, created_by=user
                )
            else:
                api_deployment: APIDeployment = APIDeployment.objects.get(pk=api_id)
            return api_deployment
        except APIDeployment.DoesNotExist:
            return None

    @staticmethod
    def send_notification(
        api: APIDeployment, workflow_execution: WorkflowExecution
    ) -> None:
        """Sends a notification for the specified API deployment and workflow
        execution.

        Args:
            api (APIDeployment): The APIDeployment instance for which the
                notification is being sent.
            workflow_execution (WorkflowExecution): The WorkflowExecution instance
                related to the notification.

        Returns:
            None
        """
        api_notification = APINotification(
            api=api, workflow_execution=workflow_execution
        )
        api_notification.send()
