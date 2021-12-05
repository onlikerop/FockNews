import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Main import zlib
from Main.models import Articles
from Main.zlib import CreateAPIRequest
from Users.models import Profile
from API.models import APIRequests, APIKey
from API.serializers import ArticleSerializer, ProfileSerializer, APIKeySerializer


# Create your views here.

def select(request):
    response = zlib.get_full_response(request, {})
    return render(request, 'API/select.html', response)


class ArticlesView(APIView):
    def get(self, request):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(
                key=request.GET['APIKey'],
                exp_datetime__gte=datetime.datetime.utcnow(),
                status="Active"
            ).first()
            if thisKey:
                counter = APIRequests.objects.filter(APIKey=thisKey).count()
                if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                    articles = Articles.objects.all()
                    serializer = ArticleSerializer(articles, many=True)
                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data)
                    )
                    APIRequest.save()
                    return Response({"articles": serializer.data if articles else None})
        return Response("403 Forbidden")

    def post(self, request):
        if "APIKey" in request.data:
            thisKey = APIKey.objects.filter(
                key=request.data.get('APIKey'),
                exp_datetime__gte=datetime.datetime.utcnow(),
                status="Active"
            ).first()
            if thisKey:
                counter = APIRequests.objects.filter(APIKey=thisKey).count()
                if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                    article = request.data.get('article')
                    # Create an article from the above data
                    serializer = ArticleSerializer(data=article)
                    if serializer.is_valid(raise_exception=True):
                        article_saved = serializer.save()

                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data)
                    )
                    APIRequest.save()
                    return Response({"success": "Article '{}' created successfully".format(article_saved.title)})
        return Response("403 Forbidden")


class ArticleView(APIView):
    def get(self, request, pk):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(
                key=request.GET['APIKey'],
                exp_datetime__gte=datetime.datetime.utcnow(),
                status="Active"
            ).first()
            if thisKey:
                counter = APIRequests.objects.filter(APIKey=thisKey).count()
                if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                    article = Articles.objects.get(id=pk)
                    serializer = ArticleSerializer(article, many=False)
                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data)
                    )
                    APIRequest.save()
                    return Response({"article": serializer.data if article else None})
        return Response("403 Forbidden")


class ProfilesView(APIView):
    def get(self, request):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(
                key=request.GET['APIKey'],
                exp_datetime__gte=datetime.datetime.utcnow(),
                status="Active"
            ).first()
            if thisKey:
                counter = APIRequests.objects.filter(APIKey=thisKey).count()
                if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                    profiles = Profile.objects.all()
                    serializer = ProfileSerializer(profiles, many=True)
                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data)
                    )
                    APIRequest.save()
                    return Response({"users": serializer.data if profiles else None})
        return Response("403 Forbidden")


class ProfileView(APIView):
    def get(self, request, pk):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(
                key=request.GET['APIKey'],
                exp_datetime__gte=datetime.datetime.utcnow(),
                status="Active"
            ).first()
            if thisKey:
                counter = APIRequests.objects.filter(APIKey=thisKey).count()
                if thisKey.allowed_requests - counter > 0 or thisKey.allowed_requests == -1:
                    user = User.objects.get(username=pk)
                    profile = Profile.objects.get(user=user)
                    serializer = ProfileSerializer(profile, many=False)
                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data)
                    )
                    APIRequest.save()
                    return Response({"user": serializer.data if profile else None})
        return Response("403 Forbidden")


class APIKeyView(APIView):
    def get(self, request, pk):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
            if thisKey:
                counter = APIRequests.objects.filter(
                    free=False,
                    APIKey=thisKey
                ).count()
                if pk == thisKey.key or thisKey.super_key:
                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data),
                        free=True
                    )
                    apikey = APIKey.objects.filter(key=pk).first()
                    serializer = APIKeySerializer(apikey, many=False)
                    response = dict()
                    response.update(serializer.data)
                    response.update({"used_times": counter})
                    APIRequest.save()
                    return Response({"APIKey": response if apikey else None})
        return Response("403 Forbidden")


class APIKeysView(APIView):
    def get(self, request):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
            if thisKey:
                if thisKey.super_key:
                    APIRequest = CreateAPIRequest(
                        APIKey=thisKey,
                        ip=zlib.get_client_ip(request),
                        body="GET: " + str(request.GET) + "\nPOST: " + str(request.POST) + "\ndata: " + str(request.data),
                        free=True
                    )
                    apikey = APIKey.objects.all()
                    serializer = APIKeySerializer(apikey, many=True)
                    response = serializer.data
                    for i in range(APIKey.objects.all().count()):
                        counter = APIRequests.objects.filter(
                            free=False,
                            APIKey=APIKey.objects.all()[i]
                        ).count()
                        response[i].update({"used_times": counter})
                    APIRequest.save()
                    return Response({"APIKeys": response if apikey else None})
        return Response("403 Forbidden")
