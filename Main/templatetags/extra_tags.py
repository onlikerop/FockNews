from datetime import datetime

from django import template
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

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


@register.simple_tag()
def check_like(user, content_type, content_id):
    try:
        if content_type.lower() == "article":
            return user.Given_rating.all().get(article_id=content_id, rating_type="Default").rating_weight
        elif content_type.lower() == "comment":
            return user.Given_commentsrating.all().get(comment_id=content_id, rating_type="Default").rating_weight
        else:
            return 0
    except ObjectDoesNotExist:
        return 0

