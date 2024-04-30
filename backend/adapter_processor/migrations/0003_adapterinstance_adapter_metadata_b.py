# Generated by Django 4.2.1 on 2024-02-13 13:09

import json
from typing import Any

from cryptography.fernet import Fernet
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("adapter_processor", "0002_adapterinstance_unique_adapter"),
    ]

    def EncryptCredentials(apps: Any, schema_editor: Any) -> None:
        encryption_secret: str = settings.ENCRYPTION_KEY
        f: Fernet = Fernet(encryption_secret.encode("utf-8"))
        AdapterInstance = apps.get_model("adapter_processor", "AdapterInstance")
        queryset = AdapterInstance.objects.all()

        for obj in queryset:  # type: ignore
            # Access attributes of the object

            print(f"Object ID: {obj.id}, Name: {obj.adapter_name}")
            if hasattr(obj, "adapter_metadata"):
                json_string: str = json.dumps(obj.adapter_metadata)
                obj.adapter_metadata_b = f.encrypt(json_string.encode("utf-8"))
                obj.save()

    operations = [
        migrations.AddField(
            model_name="adapterinstance",
            name="adapter_metadata_b",
            field=models.BinaryField(null=True),
        ),
        migrations.RunPython(
            EncryptCredentials, reverse_code=migrations.RunPython.noop
        ),
    ]
