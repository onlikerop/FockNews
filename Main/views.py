from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext


def index(request):
    return render(request, 'Main/index.html')


def contacts(request):
    return render(request, 'Main/contacts.html')
