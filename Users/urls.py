from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(
        '<slug:pk>/',
        views.userpage,
        name='userpage'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
