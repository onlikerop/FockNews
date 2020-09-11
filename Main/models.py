from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    create_datetime = models.DateTimeField()
    pub_datetime = models.DateTimeField(
        blank=True,
        null=True
    )
    lasted_datetime = models.DateTimeField(
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор'
    )
    tags = models.TextField()
    status = models.CharField(max_length=24)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Bans(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ID заблокированного пользователя',
        related_name='whom_banned'
    )
    reason = models.TextField()
    who_banned = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='ID заблокировавшего пользователя',
        related_name='who_banned'
    )
    ban_datetime = models.DateTimeField()
    pass_datetime = models.DateTimeField()
    status = models.CharField(
        max_length=24,
        blank=True,
        null=True,
        default='Active'
    )
    admin_note = models.TextField()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Блокировка'
        verbose_name_plural = 'Блокировки'


class UserData(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ID пользователя'
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/avatars'
    )
    rank = models.CharField(max_length=64)
    about_me = models.TextField()
    birthday_date = models.DateField(
        blank=True,
        null=True
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Дополнительные данные пользователя'
        verbose_name_plural = 'Дополнительные данные пользователей'
