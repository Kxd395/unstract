# Generated by Django 4.2.1 on 2024-07-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prompt_studio", "0007_remove_toolstudioprompt_assert_prompt_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="toolstudioprompt",
            name="checked_in",
            field=models.BooleanField(
                db_comment="Current checked-in prompt", default=True
            ),
        ),
    ]
