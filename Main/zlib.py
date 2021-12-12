import datetime
import string
import random

from API.models import APIKey as APIKey_M, APIKeys_Permissions, APIPermissions, APIKey

from API.models import APIRequests
from Main.models import Articles
from django.db.models import Sum, Q, Count, F, Case, When


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
            "\ndata: " + str(request.data)
            )


def genAPIKey():
    while True:
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64)).upper()
        if not APIKey_M.objects.filter(key=key).first():
            return key


def checkAPIKeyPerm(key, perm):
    if isinstance(perm, list):
        if len(perm) > 1:
            perms = []
            if isinstance(perm[0], str):
                if not perm:
                    return True
                perms.append(bool(APIPermissions.objects.filter(codename=perm).first()))
            else:
                perms = perm
            for i in range(len(perms)):
                perms[i] = APIKeys_Permissions.objects.filter(
                    key=key,
                    permission=perms[i]
                )
            return (True in perms) or key.super_key
        elif len(perm) == 1:
            perm = perm[0]
        else:
            return True
    if isinstance(perm, str):
        if not perm:
            return True
        perm = APIPermissions.objects.filter(codename=perm).first()
    if isinstance(key, str):
        key = APIKey_M.objects.filter(key=key).first()
    if not (key and perm):
        return False
    return APIKeys_Permissions.objects.filter(
        key=key,
        permission=perm
    ) or key.super_key


# This is done to automatically create the permissions used in the application in case they were lost.
def requiredPerm(perm=None, silent=False, description=None):
    if not perm:
        return None
    permissions = []
    if isinstance(perm, list):
        for i in perm:
            permission, created = APIPermissions.objects.get_or_create(codename=i)
            if created:
                if not description[i] and not silent:
                    description = input(
                        "There wasn't such permission as {}, and it was created. You can set the description or skip: ".format(
                            perm))
                if silent:
                    print("There wasn't such permission as {}, and it was created.".format(perm))
                if description[i]:
                    permission.name = description
                    permission.save()
            permissions.append(permission)
    else:
        permission, created = APIPermissions.objects.get_or_create(codename=perm)
        if created:
            if not description and not silent:
                description = input(
                    "There wasn't such permission as {}, and it was created. You can set the description or skip: ".format(
                        perm))
            if silent:
                print("There wasn't such permission as {}, and it was created.".format(perm))
            if description:
                permission.name = description
                permission.save()
            permissions.append(permission)
    return permissions


def getThisKey(request, active=True, free=False):
    return APIKey.objects.annotate(
        used_times=Count('APIRequests', filter=Q(APIRequests__free=False))
    ).filter(
        Q(exp_datetime__gte=datetime.datetime.utcnow(), status="Active") if active else Q(),
        (Q(allowed_requests=-1) | Q(used_times__lt=F('allowed_requests'))) if not free else Q(),
        key=(
            request.GET['APIKey'] if request.method == "GET"
            else request.data['APIKey']
        )
    ).first()
