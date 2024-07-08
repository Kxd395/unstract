import json
import uuid
from typing import Any

from account_v2.models import User
from connector_auth_v2.models import ConnectorAuth
from connector_processor_v2.connector_processor import ConnectorProcessor
from connector_processor_v2.constants import ConnectorKeys
from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models
from utils.models.base_model import BaseModel
from utils.models.organization_mixin import (
    DefaultOrganizationManagerMixin,
    DefaultOrganizationMixin,
)
from workflow_manager.workflow_v2.models import Workflow

from backend.constants import FieldLengthConstants as FLC

CONNECTOR_NAME_SIZE = 128
VERSION_NAME_SIZE = 64


class ConnectorInstanceModelManager(DefaultOrganizationManagerMixin, models.Manager):
    pass


class ConnectorInstance(DefaultOrganizationMixin, BaseModel):
    class ConnectorType(models.TextChoices):
        INPUT = "INPUT", "Input"
        OUTPUT = "OUTPUT", "Output"

    class ConnectorMode(models.IntegerChoices):
        UNKNOWN = 0, "UNKNOWN"
        FILE_SYSTEM = 1, "FILE_SYSTEM"
        DATABASE = 2, "DATABASE"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connector_name = models.TextField(
        max_length=CONNECTOR_NAME_SIZE, null=False, blank=False
    )
    workflow = models.ForeignKey(
        Workflow,
        on_delete=models.CASCADE,
        related_name="connector_workflow",
        null=False,
        blank=False,
    )
    connector_id = models.CharField(max_length=FLC.CONNECTOR_ID_LENGTH, default="")
    connector_metadata = models.BinaryField(null=True)
    connector_version = models.CharField(max_length=VERSION_NAME_SIZE, default="")
    connector_type = models.CharField(choices=ConnectorType.choices)
    connector_auth = models.ForeignKey(
        ConnectorAuth,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="connector_instances",
    )
    connector_mode = models.CharField(
        choices=ConnectorMode.choices,
        default=ConnectorMode.UNKNOWN,
        db_comment="0: UNKNOWN, 1: FILE_SYSTEM, 2: DATABASE",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="connectors_created",
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="connectors_modified",
        null=True,
        blank=True,
    )

    # Manager
    objects = ConnectorInstanceModelManager()

    def get_connector_metadata(self) -> dict[str, str]:
        """Gets connector metadata and refreshes the tokens if needed in case
        of OAuth."""
        tokens_refreshed = False
        if self.connector_auth:
            (
                self.connector_metadata,
                tokens_refreshed,
            ) = self.connector_auth.get_and_refresh_tokens()
        if tokens_refreshed:
            self.save()
        return self.connector_metadata

    @staticmethod
    def supportsOAuth(connector_id: str) -> bool:
        return bool(
            ConnectorProcessor.get_connector_data_with_key(
                connector_id, ConnectorKeys.OAUTH
            )
        )

    def __str__(self) -> str:
        return (
            f"Connector({self.id}, type{self.connector_type},"
            f" workflow: {self.workflow})"
        )

    @property
    def metadata(self) -> Any:
        encryption_secret: str = settings.ENCRYPTION_KEY
        cipher_suite: Fernet = Fernet(encryption_secret.encode("utf-8"))
        decrypted_value = cipher_suite.decrypt(
            bytes(self.connector_metadata).decode("utf-8")
        )
        return json.loads(decrypted_value)

    class Meta:
        db_table = "connector_instance_v2"
        verbose_name = "Connector Instance"
        verbose_name_plural = "Connector Instances"
        constraints = [
            models.UniqueConstraint(
                fields=["connector_name", "workflow", "connector_type"],
                name="unique_workflow_connector",
            ),
        ]
