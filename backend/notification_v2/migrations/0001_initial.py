# Generated by Django 4.2.1 on 2024-09-25 09:55

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("api_v2", "0001_initial"),
        ("pipeline_v2", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                    "name",
                    models.CharField(
                        db_comment="Name of the notification.",
                        default="Notification",
                        max_length=255,
                    ),
                ),
                ("url", models.URLField(null=True)),
                (
                    "authorization_key",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "authorization_header",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "authorization_type",
                    models.CharField(
                        choices=[
                            ("BEARER", "Bearer"),
                            ("API_KEY", "Api key"),
                            ("CUSTOM_HEADER", "Custom header"),
                            ("NONE", "None"),
                        ],
                        default="NONE",
                        max_length=50,
                    ),
                ),
                ("max_retries", models.IntegerField(default=0)),
                (
                    "platform",
                    models.CharField(
                        blank=True,
                        choices=[("SLACK", "Slack"), ("API", "Api")],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[("WEBHOOK", "Webhook")],
                        default="WEBHOOK",
                        max_length=50,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        db_comment="Flag indicating whether the notification is active or not.",
                        default=True,
                    ),
                ),
                (
                    "api",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to="api_v2.apideployment",
                    ),
                ),
                (
                    "pipeline",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notifications",
                        to="pipeline_v2.pipeline",
                    ),
                ),
            ],
            options={
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
                "db_table": "notification",
            },
        ),
        migrations.AddConstraint(
            model_name="notification",
            constraint=models.UniqueConstraint(
                fields=("name", "pipeline"), name="unique_name_pipeline"
            ),
        ),
        migrations.AddConstraint(
            model_name="notification",
            constraint=models.UniqueConstraint(
                fields=("name", "api"), name="unique_name_api"
            ),
        ),
    ]