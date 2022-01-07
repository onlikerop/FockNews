from datetime import datetime

from django import template
from django.contrib.auth.models import User
from django.db.models import Q

from Main.models import Articles
from Users.models import Profile, Bans

register = template.Library()


@register.simple_tag()
def check_perm(user, perm):
    return user.has_perm(perm)


@register.simple_tag()
def check_ban(user):
    is_banned = bool(Bans.objects.filter(Q(user=user)
                                         & ~Q(status='canceled')
                                         & ~Q(status='paused')
                                         & Q(pass_datetime__gt=datetime.now().strftime("%Y-%m-%d %H:%M:%d"))
                                         ).order_by("-ban_datetime").count())
    result = {
        'is_banned': is_banned
    }
    if is_banned:
        result = dict(result, data=Bans.objects.filter(Q(user=user)
                                                       & ~Q(status='canceled')
                                                       & ~Q(status='paused')
                                                       & Q(
            pass_datetime__gt=datetime.now().strftime("%Y-%m-%d %H:%M:%d"))
                                                       ).order_by("-ban_datetime")[0])
    return result


@register.simple_tag()
def sort_comments(comments, sort):
    return comments.recsort(sort)
