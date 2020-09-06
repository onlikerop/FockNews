from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from Main.models import Articles


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
    return render(request, 'Main/article.html',
                  {
                      'articles': Articles.objects.get(id=pk),
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
