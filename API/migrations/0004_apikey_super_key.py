# Generated by Django 3.1.5 on 2021-11-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_auto_20211122_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikey',
            name='super_key',
            field=models.BooleanField(default=False),
        ),
    ]