# Generated by Django 3.1.1 on 2020-09-12 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='images/avatars')),
                ('rank', models.CharField(max_length=64)),
                ('about_me', models.TextField()),
                ('birthday_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ID пользователя')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
        migrations.CreateModel(
            name='Bans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('ban_datetime', models.DateTimeField()),
                ('pass_datetime', models.DateTimeField()),
                ('status', models.CharField(blank=True, default='Active', max_length=24, null=True)),
                ('admin_note', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='whom_banned', to=settings.AUTH_USER_MODEL, verbose_name='ID заблокированного пользователя')),
                ('who_banned', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='who_banned', to=settings.AUTH_USER_MODEL, verbose_name='ID заблокировавшего пользователя')),
            ],
            options={
                'verbose_name': 'Блокировка',
                'verbose_name_plural': 'Блокировки',
            },
        ),
    ]
