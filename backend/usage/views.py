import logging

from django.db.models import Sum
from django.http import HttpRequest
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response

from .constants import UsageKeys
from .models import Usage
from .serializers import GetUsageSerializer

logger = logging.getLogger(__name__)


class UsageView(viewsets.ModelViewSet):
    """Viewset for managing Usage-related operations."""

    @action(detail=True, methods=["get"])
    def get_token_usage(self, request: HttpRequest) -> Response:
        """Retrieves the aggregated token usage for a given run_id.

        This method validates the 'run_id' query parameter, aggregates the token
        usage statistics for the specified run_id, and returns the results.

        Args:
            request (HttpRequest): The HTTP request object containing the
            query parameters.

        Returns:
            Response: A Response object containing the aggregated token usage data
                      with HTTP 200 OK status if successful, or an error message and
                      appropriate HTTP status if an error occurs.

        Raises:
            ValidationError: If the 'run_id' query parameter is missing or invalid.
            APIException: If an unexpected error occurs during the execution.
        """

        try:
            # Validate the query parameters using the serializer
            # This ensures that 'run_id' is present and valid
            serializer = GetUsageSerializer(data=self.request.query_params)
            serializer.is_valid(raise_exception=True)
            run_id = serializer.validated_data.get(UsageKeys.RUN_ID)

            # Aggregate the token counts for the given run_id
            # This uses Django's ORM to sum up the token counts
            usage_summary = Usage.objects.filter(run_id=run_id).aggregate(
                embedding_tokens=Sum("embedding_tokens"),
                prompt_tokens=Sum("prompt_tokens"),
                completion_tokens=Sum("completion_tokens"),
                total_tokens=Sum("total_tokens"),
            )

            # Prepare the result dictionary with None as the default value
            result = {
                "embedding_tokens": usage_summary.get("embedding_tokens"),
                "prompt_tokens": usage_summary.get("prompt_tokens"),
                "completion_tokens": usage_summary.get("completion_tokens"),
                "total_tokens": usage_summary.get("total_tokens"),
            }

            # Log the successful completion of the operation
            logger.info(f"Token usage retrieved successfully for run_id: {run_id}")

            # Return the result
            return Response(status=status.HTTP_200_OK, data=result)
        except ValidationError as e:
            # Handle validation errors specifically
            logger.error(f"Validation error: {e.detail}")
            raise ValidationError(detail=f"Validation error: {str(e)}")
        except Exception as e:
            # Handle any other exceptions that might occur during the execution
            error_msg = "An unexpected error occurred while fetching the token usage"
            logger.error(f"{error_msg}: {e}")
            raise APIException(detail=error_msg)
