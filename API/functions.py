import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response

from API.models import APIKey, APIRequests
from API.serializers import ArticleSerializer, ProfileSerializer, APIKeySerializer, APIRequestSerializer, BansSerializer
from Main import zlib
from Main.models import Articles
from Main.zlib import CreateAPIRequest, checkAPIKeyPerm, requiredPerm, getThisKey
from Users.models import Profile, Bans


def APIFunc(request, func, perm, **kwargs):
    if "APIKey" in request.GET.keys() if request.method == "GET" else "APIKey" in request.data:
        return func(request=request, rPerm=requiredPerm(perm), **kwargs)
    else:
        return Response("403 Forbidden")


def APIGetArticles(request, rPerm):
    thisKey = APIKey.objects.filter(
        key=request.GET['APIKey'],
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active"
    ).first()
    # print("\n" + str(thisKey) + str(getThisKey(request)) + "\n")
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                articles = Articles.objects.all()
                serializer = ArticleSerializer(articles, many=True)
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                return Response({"articles": serializer.data if articles else None})


def APIGetArticle(request, rPerm, pk):
    thisKey = APIKey.objects.filter(
        key=request.GET['APIKey'],
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active"
    ).first()
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                article = Articles.objects.get(id=pk)
                serializer = ArticleSerializer(article, many=False)
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                return Response({"article": serializer.data if article else None})


def APICreateArticle(request, rPerm):
    thisKey = APIKey.objects.filter(
        key=request.data.get('APIKey'),
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active"
    ).first()
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                article = request.data.get('article')
                # Create an article from the above data
                serializer = ArticleSerializer(data=article)
                if serializer.is_valid(raise_exception=True):
                    article_saved = serializer.save()

                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                return Response({"success": "Article '{}' created successfully".format(article_saved.title)})


def APIGetProfiles(request, rPerm):
    thisKey = APIKey.objects.filter(
        key=request.GET['APIKey'],
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active"
    ).first()
    if thisKey:
        counter = APIRequests.objects.filter(
            APIKey=thisKey,
            free=False
        ).count()
        if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
            profiles = Profile.objects.all()
            serializer = ProfileSerializer(profiles, many=True)
            APIRequest = CreateAPIRequest(
                APIKey=thisKey,
                ip=zlib.get_client_ip(request),
                body=zlib.getRequestBody(request)
            )
            APIRequest.save()
            return Response({"users": serializer.data if profiles else None})


def APIGetProfile(request, rPerm, pk):
    thisKey = APIKey.objects.filter(
        key=request.GET['APIKey'],
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active"
    ).first()
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                user = User.objects.get(username=pk)
                profile = Profile.objects.get(user=user)
                serializer = ProfileSerializer(profile, many=False)
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                return Response({"user": serializer.data if profile else None})


def APIGetKey(request, rPerm, pk):
    thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
    if thisKey:
        if pk == thisKey.key or checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            APIRequest = CreateAPIRequest(
                APIKey=thisKey,
                ip=zlib.get_client_ip(request),
                body=zlib.getRequestBody(request),
                free=True
            )
            apikey = APIKey.objects.filter(key=pk).first()
            serializer = APIKeySerializer(apikey, many=False)
            response = dict()
            response.update(serializer.data)
            response.update({"used_times": counter})
            APIRequest.save()
            return Response({"APIKey": response if apikey else None})


def APICreateKey(request, rPerm):
    thisKey = APIKey.objects.filter(
        key=request.data.get('APIKey'),
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active",
        super_key=True
    ).first()
    if thisKey:
        counter = APIRequests.objects.filter(
            APIKey=thisKey,
            free=False
        ).count()
        if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
            APIRequest = CreateAPIRequest(
                APIKey=thisKey,
                ip=zlib.get_client_ip(request),
                body=zlib.getRequestBody(request)
            )
            APIRequest.save()
            apikey = {"key": zlib.genAPIKey()}
            apikey.update(request.data.get('key'))
            # Create an APIKey from the above data
            serializer = APIKeySerializer(data=apikey)
            if serializer.is_valid(raise_exception=True):
                apikey_saved = serializer.save()
            return Response({
                "success": "APIKey '{}' created successfully for '{}'. It is valid for {} uses and will expire at {}".format(
                    apikey_saved.key,
                    apikey_saved.purpose,
                    apikey_saved.allowed_requests if apikey_saved.allowed_requests != -1 else "infinity",
                    apikey_saved.exp_datetime
                )})


def APIExtendKey(request, rPerm):
    thisKey = APIKey.objects.filter(
        key=request.data.get('APIKey'),
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active"
    ).first()
    print("\n", thisKey, getThisKey(request), "\n")
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                if "key" not in request.data:
                    return Response("449 Retry With: 'key'")
                else:
                    if not ("exp_datetime" in request.data or "additional_requests" in request.data):
                        return Response("449 Retry With: 'exp_date' or 'additional_requests'")
                    else:
                        key = APIKey.objects.get(key=request.data.get('key'))
                        if key:
                            if "exp_datetime" in request.data:
                                key.exp_datetime = request.data.get('exp_datetime')
                            if "additional_requests" in request.data:
                                key.allowed_requests += request.data.get('additional_requests')
                            key.save()
                            return Response({
                                "success": "APIKey '{}' updated successfully. Now it has {} uses and its new expiration datetime is  {}".format(
                                    key.key,
                                    key.allowed_requests,
                                    key.exp_datetime
                                )})
                        else:
                            return Response("404 Not Found")


def APIGetKeys(request, rPerm):
    thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
    if thisKey:
        if thisKey.super_key:
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                apikey = APIKey.objects.all()
                serializer = APIKeySerializer(apikey, many=True)
                response = serializer.data
                for i in range(APIKey.objects.all().count()):
                    allcounter = APIRequests.objects.filter(
                        free=False,
                        APIKey=APIKey.objects.all()[i]
                    ).count()
                    response[i].update({"used_times": allcounter})
                APIRequest.save()
                return Response({"APIKeys": response if apikey else None})


def APIGetRequests(request, rPerm):
    thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                apirequest = APIRequests.objects.all()
                serializer = APIRequestSerializer(apirequest, many=True)
                response = serializer.data
                return Response({"APIRequests": response if apirequest else None})


def APIGetBans(request, rPerm):
    thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
    if thisKey:
        if checkAPIKeyPerm(thisKey, rPerm):
            counter = APIRequests.objects.filter(
                APIKey=thisKey,
                free=False
            ).count()
            if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                APIRequest = CreateAPIRequest(
                    APIKey=thisKey,
                    ip=zlib.get_client_ip(request),
                    body=zlib.getRequestBody(request)
                )
                APIRequest.save()
                bans = Bans.objects.filter(
                    Q(user=request.GET['user']) if "user" in request.GET.keys() else Q(),
                    Q(who_banned=request.GET['who_banned']) if "who_banned" in request.GET.keys() else Q(),
                    Q(pass_datetime__gte=datetime.datetime.now(),
                      status="Active") if "active" in request.GET.keys() else Q()
                )
                serializer = BansSerializer(bans, many=True)
                response = serializer.data
                return Response({"Bans": response if bans else None})


def APICreateBan(request, rPerm):
    thisKey = APIKey.objects.filter(
        key=request.data.get('APIKey'),
        exp_datetime__gte=datetime.datetime.utcnow(),
        status="Active",
        super_key=True
    ).first()
    if thisKey:
        counter = APIRequests.objects.filter(
            APIKey=thisKey,
            free=False
        ).count()
        if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
            APIRequest = CreateAPIRequest(
                APIKey=thisKey,
                ip=zlib.get_client_ip(request),
                body=zlib.getRequestBody(request)
            )
            ban = request.data.get('ban')
            # Create an APIKey from the above data
            serializer = BansSerializer(data=ban)
            if serializer.is_valid(raise_exception=True):
                ban_saved = serializer.save()
            APIRequest.save()
            return Response({"success": "Ban for user '{}' created successfully".format(ban_saved.user)})
