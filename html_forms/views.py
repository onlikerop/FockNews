from django.shortcuts import render, redirect
from html_forms.forms import CreateArticleForm
import datetime


def contact(request):
    return render(request, 'html_forms/contact_form.html')


def createarticle(request):
    if request.method == 'POST':
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.create_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%d")
            if instance.status == "published":
                instance.pub_datetime = instance.create_datetime
            instance.save()
    return render(request, 'html_forms/create_article_form.html',
                  {
                      'form': CreateArticleForm(),
                      'user_data': request.user
                  }
                  )
