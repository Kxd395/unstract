import logging
from typing import Any, Optional

from account.custom_exceptions import DuplicateData
from django.db import IntegrityError
from django.db.models import QuerySet
from django.http import HttpRequest
from file_management.file_management_helper import FileManagerHelper
from permissions.permission import IsOwner, IsOwnerOrSharedUser
from prompt_studio.processor_loader import ProcessorConfig, load_plugins
from prompt_studio.prompt_profile_manager.constants import ProfileManagerErrors
from prompt_studio.prompt_profile_manager.models import ProfileManager
from prompt_studio.prompt_profile_manager.serializers import (
    ProfileManagerSerializer,
)
from prompt_studio.prompt_studio.constants import ToolStudioPromptErrors
from prompt_studio.prompt_studio.exceptions import FilenameMissingError
from prompt_studio.prompt_studio.serializers import ToolStudioPromptSerializer
from prompt_studio.prompt_studio_core.constants import (
    FileViewTypes,
    ToolStudioErrors,
    ToolStudioKeys,
    ToolStudioPromptKeys,
)
from prompt_studio.prompt_studio_core.exceptions import (
    IndexingError,
    ToolDeleteError,
)
from prompt_studio.prompt_studio_core.prompt_studio_helper import (
    PromptStudioHelper,
)
from prompt_studio.prompt_studio_document_manager.models import DocumentManager
from prompt_studio.prompt_studio_document_manager.prompt_studio_document_helper import (  # noqa: E501
    PromptStudioDocumentHelper,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from tool_instance.models import ToolInstance
from utils.filtering import FilterHelper

from unstract.connectors.filesystems.local_storage.local_storage import (
    LocalStorageFS,
)

from .models import CustomTool
from .serializers import (
    CustomToolSerializer,
    FileInfoIdeSerializer,
    FileUploadIdeSerializer,
    PromptStudioIndexSerializer,
    SharedUserListSerializer,
)

logger = logging.getLogger(__name__)


class PromptStudioCoreView(viewsets.ModelViewSet):
    """Viewset to handle all Custom tool related operations."""

    versioning_class = URLPathVersioning

    serializer_class = CustomToolSerializer

    processor_plugins = load_plugins()

    def get_permissions(self) -> list[Any]:
        if self.action == "destroy":
            return [IsOwner()]

        return [IsOwnerOrSharedUser()]

    def get_queryset(self) -> Optional[QuerySet]:
        filter_args = FilterHelper.build_filter_args(
            self.request,
            ToolStudioKeys.CREATED_BY,
        )
        if filter_args:
            queryset = CustomTool.objects.for_user(self.request.user).filter(
                **filter_args
            )
        else:
            queryset = CustomTool.objects.for_user(self.request.user)
        return queryset

    def create(self, request: HttpRequest) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            raise DuplicateData(
                f"{ToolStudioErrors.TOOL_NAME_EXISTS}, \
                    {ToolStudioErrors.DUPLICATE_API}"
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(
        self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> Response:
        instance: CustomTool = self.get_object()
        # Checks if tool is exported
        if hasattr(instance, "prompt_studio_registry"):
            exported_tool_instances_in_use = ToolInstance.objects.filter(
                tool_id__exact=instance.prompt_studio_registry.pk
            )
            dependent_wfs = set()
            for tool_instance in exported_tool_instances_in_use:
                dependent_wfs.add(tool_instance.workflow_id)
            if len(dependent_wfs) > 0:
                logger.info(
                    f"Cannot destroy custom tool {instance.tool_id},"
                    f" depended by workflows {dependent_wfs}"
                )
                raise ToolDeleteError(
                    "Failed to delete tool, its used in other workflows. "
                    "Delete its usages first"
                )
        return super().destroy(request, *args, **kwargs)

    def partial_update(
        self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]
    ) -> Response:
        summarize_llm_profile_id = request.data.get(
            ToolStudioKeys.SUMMARIZE_LLM_PROFILE, None
        )
        if summarize_llm_profile_id:
            prompt_tool = self.get_object()

            ProfileManager.objects.filter(
                prompt_studio_tool=prompt_tool
            ).update(is_summarize_llm=False)
            profile_manager = ProfileManager.objects.get(
                pk=summarize_llm_profile_id
            )
            profile_manager.is_summarize_llm = True
            profile_manager.save()

        return super().partial_update(request, *args, **kwargs)

    @action(detail=True, methods=["get"])
    def get_select_choices(self, request: HttpRequest) -> Response:
        """Method to return all static dropdown field values.

        The field values are retrieved from `./static/select_choices.json`.

        Returns:
            Response: Reponse of dropdown dict
        """
        try:
            select_choices: dict[
                str, Any
            ] = PromptStudioHelper.get_select_fields()
            return Response(select_choices, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error occured while fetching select fields {e}")
            return Response(select_choices, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"])
    def list_profiles(self, request: HttpRequest, pk: Any = None) -> Response:
        prompt_tool = (
            self.get_object()
        )  # Assuming you have a get_object method in your viewset

        profile_manager_instances = ProfileManager.objects.filter(
            prompt_studio_tool=prompt_tool
        )

        serialized_instances = ProfileManagerSerializer(
            profile_manager_instances, many=True
        ).data

        return Response(serialized_instances)

    @action(detail=True, methods=["patch"])
    def make_profile_default(
        self, request: HttpRequest, pk: Any = None
    ) -> Response:
        prompt_tool = (
            self.get_object()
        )  # Assuming you have a get_object method in your viewset

        ProfileManager.objects.filter(prompt_studio_tool=prompt_tool).update(
            is_default=False
        )

        profile_manager = ProfileManager.objects.get(
            pk=request.data["default_profile"]
        )
        profile_manager.is_default = True
        profile_manager.save()

        return Response(
            status=status.HTTP_200_OK,
            data={"default_profile": profile_manager.profile_id},
        )

    @action(detail=True, methods=["get"])
    def index_document(self, request: HttpRequest) -> Response:
        """API Entry point method to index input file.

        Args:
            request (HttpRequest)

        Raises:
            IndexingError
            ValidationError

        Returns:
            Response
        """
        serializer = PromptStudioIndexSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tool_id: str = serializer.validated_data.get(
            ToolStudioPromptKeys.TOOL_ID
        )
        document_id: str = serializer.validated_data.get(
            ToolStudioPromptKeys.DOCUMENT_ID
        )
        document: DocumentManager = DocumentManager.objects.get(pk=document_id)
        file_name: str = document.document_name
        unique_id = PromptStudioHelper.index_document(
            tool_id=tool_id,
            file_name=file_name,
            org_id=request.org_id,
            user_id=request.user.user_id,
            document_id=document_id,
        )

        for processor_plugin in self.processor_plugins:
            cls = processor_plugin[ProcessorConfig.METADATA][
                ProcessorConfig.METADATA_SERVICE_CLASS
            ]
            cls.process(
                tool_id=tool_id,
                file_name=file_name,
                org_id=request.org_id,
                user_id=request.user.user_id,
                document_id=document_id,
            )

        if unique_id:
            return Response(
                {"message": "Document indexed successfully."},
                status=status.HTTP_200_OK,
            )
        else:
            logger.error(
                "Error occured while indexing. Unique ID is not valid."
            )
            raise IndexingError()

    @action(detail=True, methods=["post"])
    def fetch_response(self, request: HttpRequest, pk: Any = None) -> Response:
        """API Entry point method to fetch response to prompt.

        Args:
            request (HttpRequest): _description_

        Raises:
            FilenameMissingError: _description_

        Returns:
            Response
        """
        custom_tool = self.get_object()
        tool_id: str = str(custom_tool.tool_id)
        document_id: str = request.data.get(ToolStudioPromptKeys.DOCUMENT_ID)
        document: DocumentManager = DocumentManager.objects.get(pk=document_id)
        file_name: str = document.document_name
        id: str = request.data.get(ToolStudioPromptKeys.ID)

        if not file_name or file_name == ToolStudioPromptKeys.UNDEFINED:
            logger.error("Mandatory field file_name is missing")
            raise FilenameMissingError()
        response: dict[str, Any] = PromptStudioHelper.prompt_responder(
            id=id,
            tool_id=tool_id,
            file_name=file_name,
            org_id=request.org_id,
            user_id=custom_tool.created_by.user_id,
            document_id=document_id,
        )
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def single_pass_extraction(self, request: HttpRequest) -> Response:
        """API Entry point method to fetch response to prompt.

        Args:
            request (HttpRequest): _description_

        Raises:
            FilenameMissingError: _description_

        Returns:
            Response
        """
        # TODO: Handle fetch_response and single_pass_
        # extraction using common function
        tool_id: str = request.data.get(ToolStudioPromptKeys.TOOL_ID)
        document_id: str = request.data.get(ToolStudioPromptKeys.DOCUMENT_ID)
        document: DocumentManager = DocumentManager.objects.get(pk=document_id)
        file_name: str = document.document_name

        if not file_name or file_name == ToolStudioPromptKeys.UNDEFINED:
            logger.error("Mandatory field file_name is missing")
            raise FilenameMissingError()
        response: dict[str, Any] = PromptStudioHelper.prompt_responder(
            tool_id=tool_id,
            file_name=file_name,
            org_id=request.org_id,
            user_id=request.user.user_id,
            document_id=document_id,
        )
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def list_of_shared_users(
        self, request: HttpRequest, pk: Any = None
    ) -> Response:
        # self.permission_classes = [IsOwnerOrSharedUser]
        custom_tool = (
            self.get_object()
        )  # Assuming you have a get_object method in your viewset

        serialized_instances = SharedUserListSerializer(custom_tool).data

        return Response(serialized_instances)

    @action(detail=True, methods=["post"])
    def create_prompt(self, request: HttpRequest, pk: Any = None) -> Response:
        context = super().get_serializer_context()
        serializer = ToolStudioPromptSerializer(
            data=request.data, context=context
        )
        # TODO : Handle model related exceptions.
        serializer.is_valid(raise_exception=True)
        try:
            # serializer.save()
            self.perform_create(serializer)
        except IntegrityError:
            raise DuplicateData(
                f"{ToolStudioPromptErrors.PROMPT_NAME_EXISTS}, \
                    {ToolStudioPromptErrors.DUPLICATE_API}"
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def create_profile_manager(
        self, request: HttpRequest, pk: Any = None
    ) -> Response:
        context = super().get_serializer_context()
        serializer = ProfileManagerSerializer(
            data=request.data, context=context
        )
        # TODO : Handle model related exceptions.
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            raise DuplicateData(
                f"{ProfileManagerErrors.PROFILE_NAME_EXISTS}, \
                    {ProfileManagerErrors.DUPLICATE_API}"
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def fetch_contents_ide(
        self, request: HttpRequest, pk: Any = None
    ) -> Response:
        custom_tool = self.get_object()
        serializer = FileInfoIdeSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        document_id: str = serializer.validated_data.get("document_id")
        document: DocumentManager = DocumentManager.objects.get(pk=document_id)
        file_name: str = document.document_name
        view_type: str = serializer.validated_data.get("view_type")

        filename_without_extension = file_name.rsplit(".", 1)[0]
        if view_type == FileViewTypes.EXTRACT:
            file_name = (
                f"{FileViewTypes.EXTRACT.lower()}/"
                f"{filename_without_extension}.txt"
            )
        if view_type == FileViewTypes.SUMMARIZE:
            file_name = (
                f"{FileViewTypes.SUMMARIZE.lower()}/"
                f"{filename_without_extension}.txt"
            )

        file_path = (
            file_path
        ) = FileManagerHelper.handle_sub_directory_for_tenants(
            request.org_id,
            is_create=True,
            user_id=custom_tool.created_by.user_id,
            tool_id=str(custom_tool.tool_id),
        )
        file_system = LocalStorageFS(settings={"path": file_path})
        if not file_path.endswith("/"):
            file_path += "/"
        file_path += file_name
        contents = FileManagerHelper.fetch_file_contents(file_system, file_path)
        return Response({"data": contents}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def upload_for_ide(self, request: HttpRequest, pk: Any = None) -> Response:
        custom_tool = self.get_object()
        serializer = FileUploadIdeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_files: Any = serializer.validated_data.get("file")

        file_path = FileManagerHelper.handle_sub_directory_for_tenants(
            request.org_id,
            is_create=True,
            user_id=custom_tool.created_by.user_id,
            tool_id=str(custom_tool.tool_id),
        )
        file_system = LocalStorageFS(settings={"path": file_path})

        documents = []
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name

            # Create a record in the db for the file
            document = PromptStudioDocumentHelper.create(
                tool_id=str(custom_tool.tool_id), document_name=file_name
            )
            # Create a dictionary to store document data
            doc = {
                "document_id": document.document_id,
                "document_name": document.document_name,
                "tool": document.tool.tool_id,
            }
            # Store file
            logger.info(
                f"Uploading file: {file_name}"
                if file_name
                else "Uploading file"
            )
            FileManagerHelper.upload_file(
                file_system,
                file_path,
                uploaded_file,
                file_name,
            )
            documents.append(doc)
        return Response({"data": documents})
