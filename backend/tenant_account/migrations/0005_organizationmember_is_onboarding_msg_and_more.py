# Generated by Django 4.2.1 on 2024-04-30 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tenant_account", "0004_alter_organizationmember_member_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="organizationmember",
            name="is_onboarding_msg",
            field=models.BooleanField(
                db_comment="Flag to indicate whether the onboarding messages are shown to user",
                default=True,
            ),
        ),
        migrations.AddField(
            model_name="organizationmember",
            name="is_prompt_studio_msg",
            field=models.BooleanField(
                db_comment="Flag to indicate whether the prompt studio messages are shown to user",
                default=True,
            ),
        ),
    ]
