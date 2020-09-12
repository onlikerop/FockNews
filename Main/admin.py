from django.contrib import admin
from Main.models import Articles
from Users.models import Profile, Bans


admin.site.register(Articles)
admin.site.register(Profile)
admin.site.register(Bans)
