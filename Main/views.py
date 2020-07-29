from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User
from Main.models import Articles
from html_forms.forms import DeleteArticleButtonForm


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
    if request.method == 'POST':
        form = DeleteArticleButtonForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.id = pk
            instance.title = Articles.objects.get(id=pk).title
            instance.body = Articles.objects.get(id=pk).body
            instance.create_datetime = Articles.objects.get(id=pk).create_datetime
            instance.pub_datetime = None
            instance.lasted_datetime = Articles.objects.get(id=pk).lasted_datetime
            instance.author = Articles.objects.get(id=pk).author
            instance.tags = Articles.objects.get(id=pk).tags
            instance.status = "deleted"
            instance.save()
    return render(request, 'Main/article.html',
                  {
                      'form': DeleteArticleButtonForm(),
                      'articles': Articles.objects.get(id=pk),
                      'user_data': request.user,
                      'necessary_perm': "Main.view_" + Articles.objects.get(id=pk).status
                  }
                  )
