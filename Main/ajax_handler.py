from django.http import HttpResponse, JsonResponse
from Main.models import Articles


def deletearticle(request, pk):
    if request.user.is_authenticated\
            and request.is_ajax\
            and request.POST\
            and request.user.has_perm("Main.delete_articles"):
        item = Articles.objects.filter(id=pk).update(status="deleted")
    return JsonResponse({"column_num": item})
