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

class ArticleView(APIView):
    def get(self, request):
        articles = Articles.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})


class ProfileView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response({"users": serializer.data})
