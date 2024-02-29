# Generated by Django 4.2.1 on 2024-02-29 09:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("account", "0005_encryptionsecret"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TrafficRule",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "fqdn",
                    models.CharField(
                        max_length=255,
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Enter a valid domain name.",
                                regex="^[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                            )
                        ],
                    ),
                ),
                ("app_deployment_id", models.UUIDField(editable=False)),
                (
                    "rule",
                    models.JSONField(
                        db_comment="Routing rule for the service", default=dict
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="traffic_rule_created_by",
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
                        related_name="traffic_rule_modified_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="app_deployment_org",
                        to="account.organization",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
