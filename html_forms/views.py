from django.shortcuts import render
from html_forms.forms import CreateArticleForm


def contact(request):
    return render(request, 'html_forms/contact_form.html')


def createarticle(request):
    if request.method == 'POST':
        form = CreateArticleForm(request.POST)

        if form.is_valid():
            form.save()
    return render(request, 'html_forms/create_article_form.html',
                  {
                      'form': CreateArticleForm()
                  }
                  )
