import logging
import os
from typing import Any

import azure.core.exceptions as AzureException
from adlfs import AzureBlobFileSystem

from unstract.connectors.exceptions import AzureHttpError, ConnectorError
from unstract.connectors.filesystems.unstract_file_system import UnstractFileSystem

logging.getLogger("azurefs").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class AzureCloudStorageFS(UnstractFileSystem):
    def __init__(self, settings: dict[str, Any]):
        super().__init__("AzureCloudStorageFS")
        account_name = settings.get("account_name", "")
        access_key = settings.get("access_key", "")
        self.azure_fs = AzureBlobFileSystem(
            account_name=account_name, credential=access_key
        )

    @staticmethod
    def get_id() -> str:
        return "azure_cloud_storage|1476a54a-ed17-4a01-9f8f-cb7e4cf91c8a"

    @staticmethod
    def get_name() -> str:
        return "Azure Cloud Storage"

    @staticmethod
    def get_description() -> str:
        return "Access files in your Azure Cloud Storage"

    @staticmethod
    def get_icon() -> str:
        return "/icons/connector-icons/azure_blob_storage.png"

    @staticmethod
    def get_json_schema() -> str:
        f = open(f"{os.path.dirname(__file__)}/static/json_schema.json")
        schema = f.read()
        f.close()
        return schema

    @staticmethod
    def requires_oauth() -> bool:
        return False

    @staticmethod
    def python_social_auth_backend() -> str:
        return ""

    @staticmethod
    def can_write() -> bool:
        return True

    @staticmethod
    def can_read() -> bool:
        return True

    def get_fsspec_fs(self) -> AzureBlobFileSystem:
        return self.azure_fs

    def test_credentials(self) -> bool:
        """To test credentials for Azure Cloud Storage."""
        try:
            is_dir = bool(self.get_fsspec_fs().isdir(""))
            if not is_dir:
                raise RuntimeError("Could not access root directory.")
        except Exception as e:
            raise ConnectorError(
                f"Error from Azure Cloud Storage while testing connection: {str(e)}"
            ) from e
        return True

    def upload_file_to_storage(self, source_path: str, destination_path: str) -> None:
        """Method to upload filepath from tool to destination connector
        directory.

        Args:
            source_path (str): source file path from tool
            destination_path (str): destination azure directory file path

        Raises:
            AzureHttpError: returns error for invalid directory
        """
        normalized_path = os.path.normpath(destination_path)
        fs = self.get_fsspec_fs()
        try:
            with open(source_path, "rb") as source_file:
                fs.write_bytes(normalized_path, source_file.read())
        except AzureException.HttpResponseError as e:
            self.raise_http_exception(e=e, path=normalized_path)

    def raise_http_exception(
        self, e: AzureException.HttpResponseError, path: str
    ) -> AzureHttpError:
        user_message = f"Error from Azure Cloud Storage connector. {e.reason} "
        if e.status_code == 400:
            user_message = (
                f"Error from Azure Cloud Storage connector. "
                f"Invalid resource name for path '{path}'. {e.reason}"
            )
        raise AzureHttpError(
            user_message,
            treat_as_user_message=True,
        ) from e
