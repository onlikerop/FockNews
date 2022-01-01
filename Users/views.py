from django.db.models import Sum, Q
from django.shortcuts import render
from django.contrib.auth.models import User

from Main import zlib


def userpage(request, pk):
    response = zlib.get_full_response(
        request,
        {
            'page_user_data': User.objects.select_related('profile').get(username=pk),
            'user_rating': User.objects.select_related('profile').annotate(
                user_rating=Sum('Articles__Rating__rating_weight')
            ).get(username=pk).user_rating,
            'necessary_perm': "Users.view_profile"
        }
    )
    return render(request, 'Users/user_page.html', response)
