# Generated by Django 4.0 on 2022-01-12 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_auto_20211208_2354'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='APIKeys_Permissions',
            new_name='APIKeysPermissions',
        ),
    ]
