import datetime

from django.db.models import Q, F, Value
from django.http import JsonResponse
from Main.models import Articles, Rating


def deletearticle(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.delete_articles"):
        item = Articles.objects.filter(id=pk).update(status="deleted")
    return JsonResponse({"column_num": item})


def restorearticle(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.restore_articles"):
        item = Articles.objects.filter(id=pk).update(status="published")
    return JsonResponse({"column_num": item})


def publisharticle(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.publish_articles"):
        item = Articles.objects.filter(id=pk).update(status="published")
    return JsonResponse({"column_num": item})


def saveeditedarticle(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.change_articles"):
        item = Articles.objects.filter(id=pk).update(title=request.POST.get('title'),
                                                     body=request.POST.get('body'),
                                                     tags=request.POST.get('tags'),
                                                     lasted_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                     )
    return JsonResponse({"column_num": item})


def uprate(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.give_rating"):
        item, created = Rating.objects.get_or_create(
            article=Articles.objects.filter(id=pk).first(),
            user=request.user
        )
        if created or item.status != "Active" or item.rating_weight != 1:
            item.rating_datetime = datetime.datetime.now()
            item.status = "Active"
            item.rating_weight = 1
        else:
            item.status = "Deleted"
            item.rating_weight = 0
        item.save()
    return JsonResponse({"column_num": 1})


def downrate(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.give_rating"):
        item, created = Rating.objects.get_or_create(
            article=Articles.objects.filter(id=pk).first(),
            user=request.user
        )
        if created or item.status != "Active" or item.rating_weight != -1:
            item.rating_datetime = datetime.datetime.now()
            item.status = "Active"
            item.rating_weight = -1
        else:
            item.status = "Deleted"
            item.rating_weight = 0
        item.save()
    return JsonResponse({"column_num": 1})
