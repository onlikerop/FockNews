from django.contrib import admin
from django.urls import include, path
from . import views
from django.views.generic import ListView, DetailView
from Main.models import Articles
from django.conf.urls.static import static
from django.conf import settings
from . import ajax_handler

urlpatterns = [
    path(
        '',
        views.index,
        name='index'
    ),
    path(
        'Wcs4q9rXQKsPzVYf63Ome1VM',
        admin.site.urls
    ),
    path(
        'contacts/',
        views.contacts,
        name='contacts'
    ),
    path(
        'news/<int:pk>/',
        views.article,
        name='article'
    ),
    path(
        'news/<int:pk>/delete/',
        ajax_handler.deletearticle,
        name='deletearticle'
    ),
    path(
        'forms/',
        include('html_forms.urls')
    ),
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),
]
