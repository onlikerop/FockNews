# Generated by Django 3.1.5 on 2021-01-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='views',
            name='view_type',
            field=models.CharField(default='Default', max_length=24),
        ),
        migrations.AlterField(
            model_name='views',
            name='view_weight',
            field=models.IntegerField(default=1),
        ),
    ]
