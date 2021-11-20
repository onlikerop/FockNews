from django.urls import path
from .views import ArticleView, ProfileView
from . import views


app_name = "articles"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('',
         views.select
         ),
    path('articles/',
         ArticleView.as_view()
         ),
    path('users/',
         ProfileView.as_view()
         ),
]