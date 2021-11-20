import datetime

from django.http import JsonResponse
from Main.models import Articles


def deletearticle(request, pk):
    if request.user.is_authenticated\
            and request.is_ajax\
            and request.POST\
            and request.user.has_perm("Main.delete_articles"):
        item = Articles.objects.filter(id=pk).update(status="deleted")
    return JsonResponse({"column_num": item})


def restorearticle(request, pk):
    if request.user.is_authenticated\
            and request.is_ajax\
            and request.POST\
            and request.user.has_perm("Main.restore_articles"):
        item = Articles.objects.filter(id=pk).update(status="published")
    return JsonResponse({"column_num": item})


def publisharticle(request, pk):
    if request.user.is_authenticated\
            and request.is_ajax\
            and request.POST\
            and request.user.has_perm("Main.publish_articles"):
        item = Articles.objects.filter(id=pk).update(status="published")
    return JsonResponse({"column_num": item})


def saveeditedarticle(request, pk):
    if request.user.is_authenticated\
            and request.is_ajax\
            and request.POST\
            and request.user.has_perm("Main.change_articles"):
        item = Articles.objects.filter(id=pk).update(title=request.POST.get('title'),
                                                     body=request.POST.get('body'),
                                                     tags=request.POST.get('tags'),
                                                     lasted_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                     )
    return JsonResponse({"column_num": item})
