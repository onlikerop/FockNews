from django.contrib import admin
from django.urls import include, path
from . import views
from django.views.generic import ListView, DetailView
from Main.models import Articles
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path(
        '',
        views.form,
        # Сюда нужно передать тот же словарь, что передавался при подключении этого файла в Main/urls.py
    ),
]
