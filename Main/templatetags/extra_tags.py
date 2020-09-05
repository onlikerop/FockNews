from django import template

register = template.Library()


@register.simple_tag()
def check_perm(user, perm):
    return user.has_perm(perm)
