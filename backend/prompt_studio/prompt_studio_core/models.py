import uuid

from account.models import User
from adapter_processor.models import AdapterInstance
from django.db import models
from utils.models.base_model import BaseModel


class CustomTool(BaseModel):
    """Model to store the custom tools designed in the tool studio."""

    tool_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    tool_name = models.TextField(unique=True, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    author = models.TextField(
        blank=False,
        null=False,
        db_comment="Specific to the user who created the tool.",
    )
    icon = models.TextField(
        blank=True,
        db_comment="Field to store \
            icon url for the custom tool.",
    )
    output = models.TextField(
        db_comment="Field to store the output format type.",
        blank=True,
    )
    log_id = models.UUIDField(
        default=uuid.uuid4,
        db_comment="Field to store unique log_id for polling",
    )
    preamble = models.TextField(
        blank=True, db_comment="Preamble to the prompts"
    )
    postamble = models.TextField(
        blank=True, db_comment="Appended as postable to prompts."
    )

    summarize_context = models.BooleanField(
        default=False, db_comment="Flag to summarize content"
    )
    summarize_as_source = models.BooleanField(
        default=False, db_comment="Flag to use summarized content as source"
    )
    summarize_prompt = models.TextField(
        blank=True,
        db_comment="Field to store the summarize prompt",
        unique=False,
    )
    prompt_grammer = models.JSONField(
        null=True, blank=True, db_comment="Synonymous words used in prompt"
    )
    monitor_llm = models.ForeignKey(
        AdapterInstance,
        on_delete=models.PROTECT,
        db_comment="Field to store monitor llm",
        null=True,
        blank=True,
        related_name="monitor_llm",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="tool_created_by",
        null=True,
        blank=True,
        editable=False,
    )
    modified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="tool_modified_by",
        null=True,
        blank=True,
        editable=False,
    )
    exclude_failed = models.BooleanField(
        db_comment="Flag to make the answer null if it is incorrect",
        default=True,
    )
    single_pass_extraction_mode = models.BooleanField(
        db_comment="Flag to enable or disable single pass extraction mode",
        default=True,
    )
    challenge_llm = models.ForeignKey(
        AdapterInstance,
        on_delete=models.PROTECT,
        db_comment="Field to store challenge llm",
        null=True,
        blank=True,
        related_name="challenge_llm",
    )
    enable_challenge = models.BooleanField(
        db_comment="Flag to enable or disable challenge", default=False
    )
