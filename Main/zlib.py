import datetime
import string
import random

from API.models import APIKey as APIKey_M

from API.models import APIRequests
from Main.models import Articles
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


def CreateAPIRequest(APIKey=None, ip=None, body=None, free=False):
    APIKey_M.objects.filter(
        exp_datetime__lt=datetime.datetime.now(),
        status="Active"
    ).update(status="Expired")
    return APIRequests(
        APIKey=APIKey,
        ip=ip,
        body=body,
        free=free
    )


def getRequestBody(request):
    return ("Path:" + request.get_full_path() + "\n" + request.method + ": " +
            str(request.GET if request.method == "GET"
                else request.POST if request.method == "POST"
                else request.PUT if request.method == "PUT"
                else request.DELETE if request.method == "DELETE"
                else request) +
            "\ndata: " + str(request.data))


def genAPIKey():
    while True:
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64)).upper()
        if not APIKey_M.objects.filter(key=key).first():
            return key
