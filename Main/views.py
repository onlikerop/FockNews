import re

from django.db.models import Sum
from django.shortcuts import render
from Main.models import Articles, Views
from html_forms.forms import CreateArticleForm
from Main import zlib
import datetime

from Main.models import Articles


def index(request):
    response = zlib.get_full_response(
        request,
        {
            'object_list': Articles.objects.filter(status="published").order_by("-pub_datetime")[:20]
        }
    )
    for art in response['object_list']:
        art.body = re.sub('(?!<br>|<\/?p>)<[^<]+?>', '', art.body)  # Removing all HTML tags, excluding <br>, <p>, </p>
    return render(request, 'Main/index.html', response)


def contacts(request):
    response = zlib.get_full_response(request, {})
    return render(request, 'Main/contacts.html', response)


def article(request, pk):
    viewer = request.user if request.user.is_authenticated else None
    locktimer = (datetime.datetime.now() - Views.objects.filter(
        article=Articles.objects.get(id=pk),
        user=viewer,
        user_ip=zlib.get_client_ip(request)
    ).order_by("-view_datetime")[0].view_datetime.replace(tzinfo=None)).seconds > 60 if Views.objects.filter(
        article=Articles.objects.get(id=pk),
        user=viewer,
        user_ip=zlib.get_client_ip(request)
    ).order_by("-view_datetime") else True
    if locktimer:
        view = Views(
            article=Articles.objects.get(id=pk),
            user=viewer,
            user_ip=zlib.get_client_ip(request),
            view_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        view.save()

    views = Views.objects.filter(article=Articles.objects.get(id=pk)).count()
    views_per_week = Views.objects.filter(
        article=Articles.objects.get(id=pk),
        view_datetime__gte=(datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d %H:%M:%S")
    ).count()
    rating = Articles.objects.get(id=pk).Rating.filter(status="Active")
    if rating:
        rating = rating.annotate(rating_sum=Sum('rating_weight')).first().rating_sum
    else:
        rating = 0
    response = zlib.get_full_response(
        request,
        {
            'articles': Articles.objects.get(id=pk),
            'views': views,
            'views_per_week': views_per_week,
            'rating': rating,
            'necessary_perm': "Main.view_" + Articles.objects.get(id=pk).status
        }
    )
    return render(request, 'Main/article.html', response)


def editarticle(request, pk):
    response = zlib.get_full_response(
        request,
        {
            'articles': Articles.objects.get(id=pk),
            'necessary_perm': "Main.change_articles"
        }
    )
    return render(request, 'html_forms/edit_article_form.html', response)


#  Form views  #
def contact(request):
    return render(request, 'html_forms/contact_form.html')


def createarticle(request):
    if request.method == 'POST':
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.create_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if instance.status == "published":
                instance.pub_datetime = instance.create_datetime
            instance.save()

    response = zlib.get_full_response(
        request,
        {
            'form': CreateArticleForm(),
            'necessary_perm': "Main.add_articles"
        }
    )
    return render(request, 'html_forms/create_article_form.html', response)
