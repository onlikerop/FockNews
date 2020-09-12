from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from Main.models import Articles
from Users.models import Profile, Bans
from html_forms.forms import CreateArticleForm
import datetime


def userpage(request, pk):
    return render(request, 'Users/user_page.html',
                  {
                      'page_user_data': User.objects.select_related('profile').get(username=pk),
                      'user_data': request.user,
                      'necessary_perm': "Users.view_profile"
                  }
                  )
