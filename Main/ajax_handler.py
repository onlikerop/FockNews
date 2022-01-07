import datetime

from django.http import JsonResponse
from Main.models import Articles, Rating, Comments, CommentsRating


def deletearticle(request, pk):
    item = 0
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.delete_articles"):
        item = Articles.objects.filter(id=pk).update(status="deleted")
    return JsonResponse({"column_num": item})


def restorearticle(request, pk):
    item = 0
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.restore_articles"):
        item = Articles.objects.filter(id=pk).update(status="published")
    return JsonResponse({"column_num": item})


def publisharticle(request, pk):
    item = 0
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.publish_articles"):
        item = Articles.objects.filter(id=pk).update(status="published")
    return JsonResponse({"column_num": item})


def saveeditedarticle(request, pk):
    item = 0
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
            and request.user.has_perm("Main.add_rating"):
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
    else:
        return JsonResponse({"column_num": 0})


def downrate(request, pk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.add_rating"):
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
    else:
        return JsonResponse({"column_num": 0})


def deletecomment(request, pk, sk):
    item = 0
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.delete_comments"):
        item = Comments.objects.filter(id=sk).update(status="deleted")
    return JsonResponse({"column_num": item})


def restorecomment(request, pk, sk):
    item = 0
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.restore_comments"):
        item = Comments.objects.filter(id=sk).update(status="published")
    return JsonResponse({"column_num": item})


def upratecomm(request, pk, sk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.add_commentsrating"):
        item, created = CommentsRating.objects.get_or_create(
            comment=Comments.objects.filter(id=sk).first(),
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
    else:
        return JsonResponse({"column_num": 0})


def downratecomm(request, pk, sk):
    if request.user.is_authenticated\
            and request.accepts\
            and request.POST\
            and request.user.has_perm("Main.add_commentsrating"):
        item, created = CommentsRating.objects.get_or_create(
            comment=Comments.objects.filter(id=sk).first(),
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
    else:
        return JsonResponse({"column_num": 0})
