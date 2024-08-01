import logging
from collections import OrderedDict
from typing import Any, Optional

from connector.connector_instance_helper import ConnectorInstanceHelper
from connector.models import ConnectorInstance
from connector_processor.connector_processor import ConnectorProcessor
from croniter import croniter
from pipeline.constants import PipelineConstants as PC
from pipeline.constants import PipelineKey as PK
from pipeline.models import Pipeline
from rest_framework import serializers
from scheduler.helper import SchedulerHelper
from utils.serializer_utils import SerializerUtils
from workflow_manager.endpoint.models import WorkflowEndpoint

from backend.serializers import AuditSerializer
from unstract.connectors.connectorkit import Connectorkit

logger = logging.getLogger(__name__)


class PipelineSerializer(AuditSerializer):

    class Meta:
        model = Pipeline
        fields = "__all__"

    def validate_cron_string(self, value: Optional[str] = None) -> Optional[str]:
        """Validate the cron string provided in the serializer data.

        This method is called internally by the serializer to ensure that
        the cron string is well-formed and adheres to the correct format.
        If the cron string is valid, it is returned. If the string is None
        or empty, it returns None. If the string is invalid, a
        ValidationError is raised.

        Args:
            value (Optional[str], optional): The cron string to validate.
                                             Defaults to None.

        Raises:
            serializers.ValidationError: Raised if the cron string is
                                         not in a valid format.

        Returns:
            Optional[str]: The validated cron string if it is valid,
                           otherwise None.
        """
        if value is None:
            return None
        cron_string = value.strip()
        # Check if the string is empty
        if not cron_string:
            return None

        # Validate the cron string
        try:
            croniter(cron_string)
        except Exception as error:
            logger.error(f"Invalid cron string '{cron_string}': {error}")
            raise serializers.ValidationError("Invalid cron string format.")

        return cron_string

    def create(self, validated_data: dict[str, Any]) -> Any:
        # TODO: Deduce pipeline type based on WF?
        validated_data[PK.ACTIVE] = True  # Add this as default instead?
        validated_data[PK.SCHEDULED] = True
        return super().create(validated_data)

    def save(self, **kwargs: Any) -> Pipeline:
        pipeline: Pipeline = super().save(**kwargs)
        if pipeline.cron_string is None:
            SchedulerHelper.remove_job(pipeline_id=str(pipeline.id))
        else:
            SchedulerHelper.add_or_update_job(pipeline)
        return pipeline

    def _get_name_and_icon(self, connectors: list[Any], connector_id: Any) -> Any:
        for obj in connectors:
            if obj["id"] == connector_id:
                return obj["name"], obj["icon"]
        return PC.NOT_CONFIGURED, None

    def _add_connector_data(
        self,
        repr: OrderedDict[str, Any],
        connector_instance_list: list[Any],
        connectors: list[Any],
    ) -> OrderedDict[str, Any]:
        """Adds connector Input/Output data.

        Args:
            sef (_type_): _description_
            repr (OrderedDict[str, Any]): _description_

        Returns:
            OrderedDict[str, Any]: _description_
        """
        repr[PC.SOURCE_NAME] = PC.NOT_CONFIGURED
        repr[PC.DESTINATION_NAME] = PC.NOT_CONFIGURED
        for instance in connector_instance_list:
            if instance.connector_type == "INPUT":
                repr[PC.SOURCE_NAME], repr[PC.SOURCE_ICON] = self._get_name_and_icon(
                    connectors=connectors,
                    connector_id=instance.connector_id,
                )
            if instance.connector_type == "OUTPUT":
                repr[PC.DESTINATION_NAME], repr[PC.DESTINATION_ICON] = (
                    self._get_name_and_icon(
                        connectors=connectors,
                        connector_id=instance.connector_id,
                    )
                )
            if repr[PC.DESTINATION_NAME] == PC.NOT_CONFIGURED:
                try:
                    check_manual_review = WorkflowEndpoint.objects.get(
                        workflow=instance.workflow,
                        endpoint_type=WorkflowEndpoint.EndpointType.DESTINATION,
                        connection_type=WorkflowEndpoint.ConnectionType.MANUALREVIEW,
                    )
                    if check_manual_review:
                        repr[PC.DESTINATION_NAME] = "Manual Review"
                except Exception as ex:
                    logger.debug(f"Not a Manual review destination: {ex}")

        return repr

    def to_representation(self, instance: Pipeline) -> OrderedDict[str, Any]:
        """To set Source, Destination & Agency for Pipelines."""
        repr: OrderedDict[str, Any] = super().to_representation(instance)

        connector_kit = Connectorkit()
        connectors = connector_kit.get_connectors_list()

        if SerializerUtils.check_context_for_GET_or_POST(context=self.context):
            workflow = instance.workflow
            connector_instance_list = ConnectorInstanceHelper.get_input_output_connector_instances_by_workflow(  # noqa
                workflow.id
            )
            repr[PK.WORKFLOW_ID] = workflow.id
            repr[PK.WORKFLOW_NAME] = workflow.workflow_name
            repr[PK.CRON_STRING] = repr.pop(PK.CRON_STRING)
            repr = self._add_connector_data(
                repr=repr,
                connector_instance_list=connector_instance_list,
                connectors=connectors,
            )

        return repr

    def get_connector_data(self, connector: ConnectorInstance, key: str) -> Any:
        return ConnectorProcessor.get_connector_data_with_key(
            connector.connector_id, key
        )
