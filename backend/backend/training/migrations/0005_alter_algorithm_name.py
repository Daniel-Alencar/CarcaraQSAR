# Generated by Django 4.2.7 on 2024-02-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0004_alter_algorithm_parameters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
