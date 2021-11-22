from django.urls import path
from .views import ArticlesView, ProfilesView, ArticleView, ProfileView, APIKeyView, APIKeysView
from . import views


app_name = "articles"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('',
         views.select
         ),
    path('articles/',
         ArticlesView.as_view()
         ),
    path('users/',
         ProfilesView.as_view()
         ),
    path('news/<int:pk>/',
         ArticleView.as_view()
         ),
    path('users/<slug:pk>/',
         ProfileView.as_view()
         ),
    path('APIKeys/',
         APIKeysView.as_view()
         ),
    path('APIKeys/<slug:pk>/',
         APIKeyView.as_view()
         ),
]
