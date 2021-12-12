from django.shortcuts import render
from rest_framework.views import APIView

from API.functions import *


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
        return APIFunc(
            request,
            APIGetBans,
            "API.bans.view.many"
        )

    def post(self, request):
        return APIFunc(
            request,
            APICreateBan,
            "API.bans.create"
        )
