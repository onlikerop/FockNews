from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from Main.models import Articles, UserData, Bans
from html_forms.forms import CreateArticleForm
import datetime


def userpage(request, pk):
    return render(request, 'Users/user_page.html',
                  {
                      'page_user_data': User.objects.get(username=pk),
                      'page_additional_user_data': UserData.objects.get(user=User.objects.get(username=pk)),
                      'user_data': request.user
                  }
                  )
