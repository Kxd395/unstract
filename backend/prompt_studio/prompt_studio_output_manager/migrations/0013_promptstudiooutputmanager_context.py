# Generated by Django 4.2.1 on 2024-06-27 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prompt_studio_output_manager", "0012_promptstudiooutputmanager_run_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="promptstudiooutputmanager",
            name="context",
            field=models.CharField(
                blank=True, db_comment="Field to store chucks used", null=True
            ),
        ),
    ]
