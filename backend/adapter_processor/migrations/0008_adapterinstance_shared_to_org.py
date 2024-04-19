# Generated by Django 4.2.1 on 2024-04-19 05:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "adapter_processor",
            "0007_remove_adapterinstance_is_default_userdefaultadapter",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="adapterinstance",
            name="shared_to_org",
            field=models.BooleanField(
                db_comment="Is the adapter shared to enitire org", default=False
            ),
        ),
    ]
