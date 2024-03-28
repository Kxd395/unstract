# Generated by Django 4.2.1 on 2024-02-07 19:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "prompt_studio_output_manager",
            "0002_promptstudiooutputmanager_doc_name",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="promptstudiooutputmanager",
            name="doc_name",
            field=models.CharField(
                db_comment="Field to store the document name",
                default=django.utils.timezone.now,
                editable=False,
            ),
            preserve_default=False,
        ),
    ]
