# Generated by Django 4.2.1 on 2024-07-02 12:46

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat_history", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatTranscript",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "message",
                    models.TextField(db_comment="Contains the the actual chat text"),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("USER", "USER"), ("ASSISTANT", "ASSISTANT")],
                        db_comment="Role of the messenger.",
                        default="USER",
                    ),
                ),
                (
                    "chat_history",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="chat_history_transcript",
                        to="chat_history.chathistory",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="transcript_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="transcript_modified_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
