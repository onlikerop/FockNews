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
        related_name='issued_by'
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
        related_name='APIKey'
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
