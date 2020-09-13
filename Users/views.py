from django.shortcuts import render
from django.contrib.auth.models import User


def userpage(request, pk):
    return render(request, 'Users/user_page.html',
                  {
                      'page_user_data': User.objects.select_related('profile').get(username=pk),
                      'user_data': request.user,
                      'necessary_perm': "Users.view_profile"
                  }
                  )
