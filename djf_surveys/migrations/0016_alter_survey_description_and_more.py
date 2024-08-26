# Generated by Django 4.1.13 on 2024-08-22 07:51

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('djf_surveys', '0015_termsvalidators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='description',
            field=tinymce.models.HTMLField(default='', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='success_page_content',
            field=models.TextField(blank=True, null=True, verbose_name='Success Page Content'),
        ),
    ]