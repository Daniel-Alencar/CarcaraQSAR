# Generated by Django 4.2.7 on 2024-01-03 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='shared',
            field=models.BooleanField(default=False),
        ),
    ]