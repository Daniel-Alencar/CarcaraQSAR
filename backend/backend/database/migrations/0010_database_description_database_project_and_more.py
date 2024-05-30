# Generated by Django 4.2.7 on 2024-05-30 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0013_remove_project_database'),
        ('database', '0009_csvdatabase'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='description',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='database',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_management.project'),
        ),
        migrations.AlterField(
            model_name='database',
            name='normalization',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.normalization'),
        ),
        migrations.DeleteModel(
            name='CSVDatabase',
        ),
    ]
