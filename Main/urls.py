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
        ListView.as_view(queryset=Articles.objects.all().order_by("-pub_datetime")[:20],
                         template_name="index.html")
    ),
    path(
        'contacts/',
        views.contacts,
        name='contacts'
    ),
    path(
        'news/<int:pk>/',
        DetailView.as_view(model=Articles,
                           template_name="article.html"),
        name='article'
    )
]
