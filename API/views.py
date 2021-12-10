from django.db.models import Q
from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView

from API.functions import *
from API.serializers import BansSerializer
from Users.models import Bans


# Create your views here.

def select(request):
    response = zlib.get_full_response(request, {})
    return render(request, 'API/select.html', response)


class ArticlesView(APIView):
    def get(self, request):
        return APIFunc(
            request,
            APIGetArticles,
            "API.articles.view.many"
        )

    def post(self, request):
        return APIFunc(
            request,
            APICreateArticle,
            "API.articles.create"
        )


class ArticleView(APIView):
    def get(self, request, pk):
        return APIFunc(
            request,
            APIGetArticle,
            "API.articles.view",
            pk=pk
        )


class ProfilesView(APIView):
    def get(self, request):
        return APIFunc(
            request,
            APIGetProfiles,
            "API.profiles.view.many"
        )


class ProfileView(APIView):
    def get(self, request, pk):
        return APIFunc(
            request,
            APIGetProfile,
            "API.profiles.view",
            pk=pk
        )


class APIKeyView(APIView):
    def get(self, request, pk=None):
        return APIFunc(
            request,
            APIGetKey,
            ["API.apikeys.view.other", "API.apikeys.view.many"],
            pk=pk
        )

    def post(self, request):
        return APIFunc(
            request,
            APIExtendKey if "extend" in request.data else APICreateKey,
            "API.apikeys.extend" if "extend" in request.data else "API.apikeys.create"
        )


class APIKeysView(APIView):
    def get(self, request):
        return APIFunc(
            request,
            APIGetKeys,
            "API.apikeys.view.many"
        )


class APIRequestsView(APIView):
    def get(self, request):
        return APIFunc(
            request,
            APIGetRequests,
            "API.apirequests.view.many"
        )


class BansView(APIView):
    def get(self, request):
        if "APIKey" in request.GET.keys():
            thisKey = APIKey.objects.filter(key=request.GET['APIKey']).first()
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
                    bans = Bans.objects.filter(
                        Q(user=request.GET['user']) if "user" in request.GET.keys() else Q(),
                        Q(who_banned=request.GET['who_banned']) if "who_banned" in request.GET.keys() else Q(),
                        Q(pass_datetime__gte=datetime.datetime.now(),
                          status="Active") if "active" in request.GET.keys() else Q()
                    )
                    serializer = BansSerializer(bans, many=True)
                    response = serializer.data
                    return Response({"Bans": response if bans else None})
        return Response("403 Forbidden")

    def post(self, request):
        if "APIKey" in request.data:
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
        return Response("403 Forbidden")
