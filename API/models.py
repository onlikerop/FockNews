from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class APIKey(models.Model):
    key = models.CharField(
        max_length=64,
        unique=True
    )
    issue_datetime = models.DateTimeField(auto_now_add=True)
    exp_datetime = models.DateTimeField()
    issued_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='ID выпустившего API-key',
        related_name='APIKey'
    )
    purpose = models.TextField()
    allowed_requests = models.IntegerField(default=100)
    status = models.CharField(
        max_length=24,
        default='Active'
    )
    super_key = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        verbose_name = 'API-key'
        verbose_name_plural = 'API-keys'

    def __str__(self):
        return self.purpose


class APIRequests(models.Model):
    APIKey = models.ForeignKey(
        APIKey,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Api-key',
        related_name='APIRequests'
    )
    ip = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    datetime = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    free = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        verbose_name = 'API запрос'
        verbose_name_plural = 'API запросы'

    def __str__(self):
        return self.datetime


class APIPermissions(models.Model):
    codename = models.CharField(
        max_length=64,
        unique=True
    )
    name = models.TextField()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Право API'
        verbose_name_plural = 'Права API'

    def __str__(self):
        return self.codename


class APIKeys_Permissions(models.Model):
    key = models.ForeignKey(
        APIKey,
        on_delete=models.PROTECT,
        verbose_name='Api-key',
        related_name='APIKeys_Permissions'
    )
    permission = models.ForeignKey(
        APIPermissions,
        on_delete=models.PROTECT,
        verbose_name='API permission',
        related_name='APIKeys_Permissions'
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Отношение права API'
        verbose_name_plural = 'Отношения прав API'
        unique_together = ['key', 'permission']

    def __str__(self):
        return str(self.key) + " - " + str(self.permission)
