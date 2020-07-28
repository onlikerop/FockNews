from django import template
import re

register = template.Library()


@register.simple_tag()
def check_perm(user, perm):
    return user.has_perm(perm)
