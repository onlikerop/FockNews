from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


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
            ("view_deleted", "Can view deleted Articles")
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
        unique_together = ('article', 'user')


class Comments(models.Model):
    article = models.ForeignKey(
        Articles,
        on_delete=models.PROTECT,
        verbose_name='Статья',
        related_name='Comments'
    )
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        default=None,
        verbose_name='Ответ на',
        related_name='Replies'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='Comments'
    )
    comment = models.TextField()
    comment_datetime = models.DateTimeField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=24,
        default='published'
    )
    objects = models.Manager()

    def __str__(self):
        return str(self.user) + ": " + str(self.article) + "[{}]".format(self.comment_datetime)

    class Meta:
        verbose_name = 'Комменатрий'
        verbose_name_plural = 'Комментарии'

        permissions = (
            ("restore_comments", "Can restore Comments"),
            ("view_deleted", "Can view deleted Comments")
        )


class CommentsRating(models.Model):
    comment = models.ForeignKey(
        Comments,
        on_delete=models.PROTECT,
        verbose_name='Комменатрий',
        related_name='Rating'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='Given_commentsrating'
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
        return "(" + str(self.comment) + "): " + "{:+}".format(self.rating_weight)

    class Meta:
        verbose_name = 'Рейтинг комменатрия'
        verbose_name_plural = 'Рейтинг комменатриев'
        unique_together = ('comment', 'user')


class Reportable(models.Model):
    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = obj

    article = models.ForeignKey(
        Articles,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Статья',
        related_name='Reported'
    )
    comment = models.ForeignKey(
        Comments,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name='Комменатрий',
        related_name='Reported'
    )

    @property
    def object(self):
        def coalesce(*args):
            for el in args:
                if el is not None:
                    return el
            return None
        return coalesce(self.article, self.comment)

    @object.setter
    def object(self, obj):
        if isinstance(obj, Articles):
            self.article = obj
            self.comment = None
        elif isinstance(obj, Comments):
            self.comment = obj
            self.article = None
        else:
            raise TypeError("Not a Reportable model")

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(article=None) | Q(comment=None), name='one_field_none'),
        ]


class Reports(models.Model):
    object = models.ForeignKey(
        Reportable,
        on_delete=models.PROTECT,
        verbose_name='Объект жалобы',
        related_name='Reports'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='Reported'
    )
    comment = models.TextField()
    report_datetime = models.DateTimeField(
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=24,
        default='Open'
    )
    objects = models.Manager()

    def __str__(self):
        return str(self.user) + ": " + str(self.object)

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'

        permissions = (
            ("consider_reports", "Can consider Reports"),
            ("review_reports", "Can review Reports")
        )
