# Generated by Django 4.2.7 on 2024-08-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0017_training_task_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootstrapvalues',
            name='R2_value',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='bootstrapvalues',
            name='R_value',
            field=models.FloatField(null=True),
        ),
    ]
