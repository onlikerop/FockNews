# Generated by Django 4.0 on 2022-01-05 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0012_comments_alter_rating_options_commentsrating'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
