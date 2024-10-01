# Generated by Django 4.2.1 on 2024-07-29 09:16

import uuid

import django.db.models.deletion
import social_django.storage
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ConnectorAuth",
            fields=[
                ("provider", models.CharField(max_length=32)),
                ("uid", models.CharField(db_index=True, max_length=255)),
                ("extra_data", models.JSONField(default=dict)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
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
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connector_auths",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Connector Auth",
                "verbose_name_plural": "Connector Auths",
                "db_table": "connector_auth",
            },
            bases=(models.Model, social_django.storage.DjangoUserMixin),
        ),
        migrations.AddConstraint(
            model_name="connectorauth",
            constraint=models.UniqueConstraint(
                fields=("provider", "uid"), name="unique_provider_uid_index"
            ),
        ),
    ]
