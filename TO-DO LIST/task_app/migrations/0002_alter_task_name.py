# Generated by Django 4.2.6 on 2023-11-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=65, verbose_name='Task name'),
        ),
    ]
