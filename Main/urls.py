import random
import string

from django.contrib import admin
from django.urls import include, path
from . import views
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
        ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(24)),
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
        'news/<int:pk>/restore/',
        ajax_handler.restorearticle,
        name='restorearticle'
    ),
    path(
        'news/<int:pk>/publish/',
        ajax_handler.publisharticle,
        name='publisharticle'
    ),
    path(
        'news/<int:pk>/edit/',
        views.editarticle,
        name='editarticle'
    ),
    path(
        'news/<int:pk>/edit/save/',
        ajax_handler.saveeditedarticle,
        name='saveeditedarticle'
    ),
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),
    path(
        'contact/',
        views.contact,
        name='contact'
    ),
    path(
        'createarticle/',
        views.createarticle,
        name='createarticle'
    ),
    path(
        'users/',
        include('Users.urls'),
        name='Users'
    ),
    path(
        'api/',
        include('API.urls'),
        name='API'
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
