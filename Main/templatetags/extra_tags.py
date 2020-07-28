from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def check_perm(**kwargs):
    user = kwargs['user']
    perm = kwargs['perm']
    return user.has_perm(perm)
