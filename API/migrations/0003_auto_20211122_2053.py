# Generated by Django 3.1.5 on 2021-11-22 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20211122_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
