# Generated by Django 4.2.6 on 2024-07-22 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("djf_surveys", "0014_alter_survey_success_page_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="TermsValidators",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("terms", models.JSONField(default=dict, verbose_name="terms")),
                (
                    "question",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="djf_surveys.question",
                        verbose_name="question",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]