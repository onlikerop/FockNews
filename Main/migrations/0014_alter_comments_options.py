# Generated by Django 4.0 on 2022-01-06 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0013_comments_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'permissions': (('restore_comments', 'Can restore Comments'), ('view_deleted', 'Can view deleted Comments')), 'verbose_name': 'Комменатрий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
