from django.shortcuts import render, redirect
from html_forms.forms import CreateArticleForm
import datetime


def contact(request):
    return render(request, 'html_forms/contact_form.html')


def createarticle(request):
    if request.method == 'POST':
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('index')
    return render(request, 'html_forms/create_article_form.html',
                  {
                      'form': CreateArticleForm(),
                      'user_data': request.user
                  }
                  )
