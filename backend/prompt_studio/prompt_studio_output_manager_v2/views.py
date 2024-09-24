import logging
from typing import Any, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpRequest
from prompt_studio.prompt_studio_output_manager_v2.constants import (
    PromptOutputManagerErrorMessage,
    PromptStudioOutputManagerKeys,
)
from prompt_studio.prompt_studio_output_manager_v2.serializers import (
    PromptStudioOutputSerializer,
)
from prompt_studio.prompt_studio_v2.models import ToolStudioPrompt
from rest_framework import status, viewsets
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from utils.common_utils import CommonUtils
from utils.filtering import FilterHelper

from .models import PromptStudioOutputManager

logger = logging.getLogger(__name__)


class PromptStudioOutputView(viewsets.ModelViewSet):
    versioning_class = URLPathVersioning
    queryset = PromptStudioOutputManager.objects.all()
    serializer_class = PromptStudioOutputSerializer

    def get_queryset(self) -> Optional[QuerySet]:
        filter_args = FilterHelper.build_filter_args(
            self.request,
            PromptStudioOutputManagerKeys.TOOL_ID,
            PromptStudioOutputManagerKeys.PROMPT_ID,
            PromptStudioOutputManagerKeys.PROFILE_MANAGER,
            PromptStudioOutputManagerKeys.DOCUMENT_MANAGER,
            PromptStudioOutputManagerKeys.IS_SINGLE_PASS_EXTRACT,
        )

        # Get the query parameter for "is_single_pass_extract"
        is_single_pass_extract_param = self.request.GET.get(
            PromptStudioOutputManagerKeys.IS_SINGLE_PASS_EXTRACT, "false"
        )

        # Convert the string representation to a boolean value
        is_single_pass_extract = CommonUtils.str_to_bool(is_single_pass_extract_param)

        filter_args[PromptStudioOutputManagerKeys.IS_SINGLE_PASS_EXTRACT] = (
            is_single_pass_extract
        )

        if filter_args:
            queryset = PromptStudioOutputManager.objects.filter(**filter_args)

        return queryset

    def get_output_for_tool_default(self, request: HttpRequest) -> Response:
        # TODO: Setup Serializer here
        # Get the tool_id from request parameters
        tool_id = request.GET.get("tool_id")
        document_manager_id = request.GET.get("document_manager")
        tool_validation_message = PromptOutputManagerErrorMessage.TOOL_VALIDATION
        tool_not_found = PromptOutputManagerErrorMessage.TOOL_NOT_FOUND
        if not tool_id:
            raise APIException(detail=tool_validation_message, code=400)

        try:
            # Fetch ToolStudioPrompt records based on tool_id
            tool_studio_prompts = ToolStudioPrompt.objects.filter(tool_id=tool_id)
        except ObjectDoesNotExist:
            raise APIException(detail=tool_not_found, code=400)

        # Initialize the result dictionary
        result: dict[str, Any] = {}

        # Iterate over ToolStudioPrompt records
        for tool_prompt in tool_studio_prompts:
            prompt_id = str(tool_prompt.prompt_id)
            profile_manager_id = str(tool_prompt.profile_manager.profile_id)

            # If profile_manager is not set, skip this record
            if not profile_manager_id:
                result[tool_prompt.prompt_key] = ""
                continue

            try:
                queryset = PromptStudioOutputManager.objects.filter(
                    prompt_id=prompt_id,
                    profile_manager=profile_manager_id,
                    is_single_pass_extract=False,
                    document_manager_id=document_manager_id,
                )

                if not queryset.exists():
                    result[tool_prompt.prompt_key] = ""
                    continue

                for output in queryset:
                    result[tool_prompt.prompt_key] = output.output
            except ObjectDoesNotExist:
                result[tool_prompt.prompt_key] = ""

        return Response(result, status=status.HTTP_200_OK)
