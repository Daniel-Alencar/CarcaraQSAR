# Generated by Django 4.2.7 on 2024-08-19 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('variables_selection', '0007_variablesselection_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='variablesselection',
            name='model_parameters',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
