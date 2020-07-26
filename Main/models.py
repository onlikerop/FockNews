from django.db import models


class Articles(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    create_datetime = models.DateTimeField()
    pub_datetime = models.DateTimeField(blank=True, null=True)
    lasted_datetime = models.DateTimeField(blank=True, null=True)
    author = models.CharField(max_length=24)
    tags = models.TextField()
    status = models.CharField(max_length=24)
    objects = models.Manager()

    def __str__(self):
        return self.title
