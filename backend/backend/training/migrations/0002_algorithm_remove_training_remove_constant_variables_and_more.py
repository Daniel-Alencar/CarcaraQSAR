# Generated by Django 4.2.7 on 2024-02-05 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0012_alter_project_database'),
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('random_forest', 'Random Forest'), ('svm', 'Support Vector Machine (SVM)'), ('linear_regression', 'Linear Regression')], max_length=200, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='training',
            name='remove_constant_variables',
        ),
        migrations.CreateModel(
            name='LinearRegression',
            fields=[
                ('algorithm_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='training.algorithm')),
                ('regularization', models.FloatField()),
            ],
            bases=('training.algorithm',),
        ),
        migrations.CreateModel(
            name='RandomForest',
            fields=[
                ('algorithm_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='training.algorithm')),
                ('num_trees', models.IntegerField()),
                ('max_depth', models.IntegerField()),
            ],
            bases=('training.algorithm',),
        ),
        migrations.CreateModel(
            name='SVM',
            fields=[
                ('algorithm_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='training.algorithm')),
                ('kernel', models.CharField(max_length=50)),
                ('C_parameter', models.FloatField()),
            ],
            bases=('training.algorithm',),
        ),
        migrations.CreateModel(
            name='VariablesSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('algorithm', models.CharField(max_length=200)),
                ('remove_constant_variables', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_management.project')),
            ],
        ),
        migrations.AlterField(
            model_name='training',
            name='algorithm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.algorithm'),
        ),
    ]