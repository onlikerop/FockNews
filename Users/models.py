from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bans(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='ID заблокированного пользователя',
        related_name='whom_banned'
    )
    reason = models.TextField(blank=True)
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
    admin_note = models.TextField(blank=True)
    objects = models.Manager()

    class Meta:
        verbose_name = 'Блокировка'
        verbose_name_plural = 'Блокировки'

    def __str__(self):
        return str(self.user) + " [" + str(self.ban_datetime) + "]"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='ID пользователя'
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='images/avatars'
    )
    rank = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )
    about_me = models.TextField(blank=True)
    birthday_date = models.DateField(
        blank=True,
        null=True
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
