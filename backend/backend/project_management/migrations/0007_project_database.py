# Generated by Django 4.2.7 on 2024-01-19 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0006_remove_project_database'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='database',
            field=models.FileField(default=None, null=True, upload_to='databases/'),
        ),
    ]
