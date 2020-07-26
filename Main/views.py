from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from Main.models import Articles


def index(request):
    return render(request, 'Main/index.html',
                  {
                      'object_list': Articles.objects.all().order_by("-pub_datetime")[:20],
                      'user_data': request.user
                  }
                  )


def contacts(request):
    return render(request, 'Main/contacts.html',
                  {
                      'user_data': request.user
                  }
                  )
