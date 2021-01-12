from django.shortcuts import render
from Main.models import Articles, Views
from html_forms.forms import CreateArticleForm
import datetime
import Main.zlib as zlib


def index(request):
    return render(request, 'Main/index.html',
                  {
                      'object_list': Articles.objects.filter(status="published").order_by("-pub_datetime")[:20],
                      'user_data': request.user
                  }
                  )


def contacts(request):
    return render(request, 'Main/contacts.html',
                  {
                      'user_data': request.user
                  }
                  )


def article(request, pk):
    viewer = request.user if request.user.is_authenticated else None
    locktimer = (datetime.datetime.utcnow() - Views.objects.filter(
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

    views = Views.objects.filter(article=Articles.objects.get(id=pk)).count
    views_per_week = Views.objects.filter(
        article=Articles.objects.get(id=pk),
        view_datetime__gte=(datetime.datetime.now() + datetime.timedelta(days=-7)).strftime("%Y-%m-%d %H:%M:%S")
    ).count
    return render(request, 'Main/article.html',
                  {
                      'articles': Articles.objects.get(id=pk),
                      'views': views,
                      'views_per_week': views_per_week,
                      'user_data': request.user,
                      'necessary_perm': "Main.view_" + Articles.objects.get(id=pk).status
                  }
                  )


def editarticle(request, pk):
    return render(request, 'html_forms/edit_article_form.html',
                  {
                      'articles': Articles.objects.get(id=pk),
                      'user_data': request.user,
                      'necessary_perm': "Main.change_articles"
                  }
                  )


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
    return render(request, 'html_forms/create_article_form.html',
                  {
                      'form': CreateArticleForm(),
                      'user_data': request.user,
                      'necessary_perm': "Main.add_articles"
                  }
                  )
