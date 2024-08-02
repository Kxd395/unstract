import uuid

from api.models import APIDeployment
from django.db import models
from pipeline.models import Pipeline
from utils.models.base_model import BaseModel

from .enums import AuthorizationType, NotificationType, PlatformType


class Notification(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(null=True)  # URL for webhook or other endpoints
    authorization_key = models.CharField(
        max_length=255, blank=True, null=True
    )  # Authorization Key or API Key
    authorization_header = models.CharField(
        max_length=255, blank=True, null=True
    )  # Header Name for custom headers
    authorization_type = models.CharField(
        max_length=50,
        choices=AuthorizationType.choices(),
        default=AuthorizationType.NONE.value,
    )
    max_retries = models.IntegerField(default=0)  # Timeout in seconds
    platform = models.CharField(
        max_length=50,
        choices=PlatformType.choices(),
        blank=True,
        null=True,
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NotificationType.choices(),
        default=NotificationType.WEBHOOK.value,
    )
    is_active = models.BooleanField(
        default=True,
        db_comment="Flag indicating whether the notification is active or not.",
    )
    # Foreign keys to specific models
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    api = models.ForeignKey(
        APIDeployment,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        # Validation for platforms
        valid_platforms = NotificationType(self.notification_type).get_valid_platforms()
        if self.platform and self.platform not in valid_platforms:
            raise ValueError(
                f"Invalid platform '{self.platform}' for notification type "
                f"'{self.notification_type}'. "
                f"Valid options are: {', '.join(valid_platforms)}."
            )

        # Allow saving only if the platform is valid or not required
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"Notification {self.id}: (Type: {self.notification_type}, "
            f"Platform: {self.platform}, Url: {self.url}))"
        )
