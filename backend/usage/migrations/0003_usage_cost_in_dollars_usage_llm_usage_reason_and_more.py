# Generated by Django 4.2.1 on 2024-06-26 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("usage", "0002_alter_usage_adapter_instance_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usage",
            name="cost_in_dollars",
            field=models.FloatField(
                db_comment="Total number of tokens used", default=0.0
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="usage",
            name="llm_usage_reason",
            field=models.CharField(
                blank=True,
                choices=[
                    ("extraction", "extraction"),
                    ("challenge", "challenge"),
                    ("summarize", "summarize"),
                ],
                db_comment="Reason for LLM usage. Empty if usage_type is 'embedding'. ",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="usage",
            name="usage_type",
            field=models.CharField(
                choices=[("llm", "llm"), ("embedding", "embedding")],
                db_comment="Type of usage, either 'llm' or 'embedding'",
                max_length=255,
            ),
        ),
        migrations.AddIndex(
            model_name="usage",
            index=models.Index(fields=["run_id"], name="token_usage_run_id_cd3578_idx"),
        ),
    ]
