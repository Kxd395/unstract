import logging

from django.db.models import Count
from usage_v2.helper import UsageHelper

from backend.serializers import AuditSerializer

from .models import PromptStudioOutputManager

logger = logging.getLogger(__name__)


class PromptStudioOutputSerializer(AuditSerializer):
    class Meta:
        model = PromptStudioOutputManager
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            token_usage = UsageHelper.get_aggregated_token_count(instance.run_id)
        except Exception as e:
            logger.error(
                "Error occured while fetching token usage for run_id"
                f"{instance.run_id}: {e}"
            )
            token_usage = {}
        data["token_usage"] = token_usage
        # Get the coverage for the current tool_id and profile_manager_id
        try:
            # Fetch all relevant outputs for the current tool and profile
            prompt_outputs = (
                PromptStudioOutputManager.objects.filter(
                    tool_id=instance.tool_id,
                    profile_manager_id=instance.profile_manager_id,
                    prompt_id=instance.prompt_id,
                )
                .values("prompt_id", "profile_manager_id")
                .annotate(document_count=Count("document_manager_id"))
            )

            coverage = {}
            for prompt_output in prompt_outputs:
                prompt_key = str(prompt_output["prompt_id"])
                profile_key = str(prompt_output["profile_manager_id"])
                coverage[f"coverage_{prompt_key}_{profile_key}"] = prompt_output[
                    "document_count"
                ]

            data["coverage"] = coverage
        except Exception as e:
            logger.error(
                "Error occurred while fetching "
                f"coverage for tool_id {instance.tool_id} "
                f"and profile_manager_id {instance.profile_manager_id}: {e}"
            )
            data["coverage"] = {}
        return data
