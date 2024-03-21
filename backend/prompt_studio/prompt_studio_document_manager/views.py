from typing import Optional

from django.db.models import QuerySet
from prompt_studio.permission import IsDocumentMangerAccesible
from prompt_studio.prompt_studio_document_manager.serializers import (
    PromptStudioDocumentManagerSerializer,
)
from prompt_studio.prompt_studio_output_manager.constants import (
    PromptStudioOutputManagerKeys,
)
from rest_framework import viewsets
from rest_framework.versioning import URLPathVersioning
from utils.filtering import FilterHelper

from .models import DocumentManager


class PromptStudioDocumentManagerView(viewsets.ModelViewSet):
    versioning_class = URLPathVersioning
    queryset = DocumentManager.objects.all()
    serializer_class = PromptStudioDocumentManagerSerializer
    permission_classes: list[type[IsDocumentMangerAccesible]] = [
        IsDocumentMangerAccesible
    ]

    def get_queryset(self) -> Optional[QuerySet]:
        filter_args = FilterHelper.build_filter_args(
            self.request,
            PromptStudioOutputManagerKeys.TOOL_ID,
        )
        queryset = None
        if filter_args:
            queryset = DocumentManager.objects.filter(**filter_args)

        return queryset
