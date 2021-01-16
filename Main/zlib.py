import datetime

from Main.models import Articles, Views
from django.db.models import Sum

# Service Functions
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def stdict(request):
    poparts = Articles.objects.filter(
        views__view_datetime__gte=(datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d %H:%M:%S")
    ).annotate(views_num=Sum('views__view_weight')).order_by('-views_num')[:3]
    return {
        'user_data': request.user,
        'sidebar_data': {
            'pop_arts': poparts
        }
    }


def get_full_response(request, addictive):
    addictive.update(stdict(request))
    return addictive
