from django.db import models
from django.contrib.auth.models import User


class Articles(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField(blank=True)
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
        verbose_name='Автор',
        related_name='Articles'
    )
    tags = models.TextField(blank=True)
    status = models.CharField(max_length=24)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

        permissions = (
            ("restore_articles", "Can restore Articles"),
            ("publish_articles", "Can publish drafts of Articles"),
            ("view_published", "Can view published Articles"),
            ("view_draft", "Can view drafts of Articles"),
            ("view_deleted", "Can view deleted Articles"),
        )


class Views(models.Model):
    article = models.ForeignKey(
        Articles,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Статья',
        related_name='Views'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь'
    )
    user_ip = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    view_datetime = models.DateTimeField(
        blank=True,
        null=True
    )
    view_type = models.CharField(
        max_length=24,
        default='Default'
    )
    view_weight = models.IntegerField(default=1)
    objects = models.Manager()

    def __str__(self):
        return self.view_datetime

    class Meta:
        verbose_name = 'Просмотры'
        verbose_name_plural = 'Просмотры'


class Rating(models.Model):
    article = models.ForeignKey(
        Articles,
        on_delete=models.PROTECT,
        verbose_name='Статья',
        related_name='Rating'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='Given_rating'
    )
    rating_datetime = models.DateTimeField(
        blank=True,
        null=True
    )
    rating_type = models.CharField(
        max_length=24,
        default='Default'
    )
    rating_weight = models.IntegerField(default=1)
    status = models.CharField(
        max_length=24,
        default='Active'
    )
    objects = models.Manager()

    def __str__(self):
        return str(self.article) + ": " + "{:+}".format(self.rating_weight)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

        permissions = (
            ("give_rating", "Can give rating to articles"),
            ("manage_rating", "Can manage rating of articles")
        )
        unique_together = ('article', 'user')
