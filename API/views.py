from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from Main import zlib
from Main.models import Articles
from Users.models import Profile
from API.serializers import ArticleSerializer, ProfileSerializer, UserSerializer


# Create your views here.

def select(request):
    response = zlib.get_full_response(request, {})
    return render(request, 'API/select.html', response)


class ArticlesView(APIView):
    def get(self, request):
        articles = Articles.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})


class ArticleView(APIView):
    def get(self, request, pk):
        article = Articles.objects.get(id=pk)
        serializer = ArticleSerializer(article, many=False)
        return Response({"article": serializer.data})


class ProfilesView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({"users": serializer.data})


class ProfileView(APIView):
    def get(self, request, pk):
        user = User.objects.get(username=pk)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, many=False)
        return Response({"user": serializer.data})
