import datetime
import string
import random

from API.models import APIKey as APIKey_M, APIKeys_Permissions, APIPermissions

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


def checkAPIKeyPerm(key, perm):
    key = APIKey_M.objects.filter(key=key).first()
    perm = APIPermissions.objects.filter(codename=perm).first()
    if not (key and perm):
        return False
    return APIKeys_Permissions.objects.filter(
        key=key,
        permission=perm
    ) or key.super_key


# This is done to automatically create the permissions used in the application in case they were lost.
def requiredPerm(perm, silent=False, description=None):
    permission, created = APIPermissions.objects.get_or_create(codename=perm)
    if created:
        if not description and not silent:
            description = input("There wasn't such permission as {}, and it was created. You can set the description or skip: ".format(perm))
        if silent:
            print("There wasn't such permission as {}, and it was created.".format(perm))
        if description:
            permission.name = description
            permission.save()
    return permission
