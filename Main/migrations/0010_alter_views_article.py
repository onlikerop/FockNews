# Generated by Django 4.0 on 2021-12-31 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_rating_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='views',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Views', to='Main.articles', verbose_name='Статья'),
        ),
    ]
