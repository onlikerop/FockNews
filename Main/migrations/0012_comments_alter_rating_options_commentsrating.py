# Generated by Django 4.0 on 2022-01-04 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Main', '0011_alter_articles_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_datetime', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(default='published', max_length=24)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Comments', to='Main.articles', verbose_name='Статья')),
                ('reply_to', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Replies', to='Main.comments', verbose_name='Ответ на')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Comments', to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Комменатрии',
                'verbose_name_plural': 'Комментарий',
            },
        ),
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'Рейтинг', 'verbose_name_plural': 'Рейтинг'},
        ),
        migrations.CreateModel(
            name='CommentsRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_datetime', models.DateTimeField(blank=True, null=True)),
                ('rating_type', models.CharField(default='Default', max_length=24)),
                ('rating_weight', models.IntegerField(default=1)),
                ('status', models.CharField(default='Active', max_length=24)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Rating', to='Main.comments', verbose_name='Комменатрий')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Given_commentsrating', to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг комменатрия',
                'verbose_name_plural': 'Рейтинг комменатриев',
                'unique_together': {('comment', 'user')},
            },
        ),
    ]
