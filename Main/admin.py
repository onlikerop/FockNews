from django.contrib import admin
from Main.models import Articles, Views
from Users.models import Profile, Bans

# Main
admin.site.register(Articles)
admin.site.register(Views)

# Users
admin.site.register(Profile)
admin.site.register(Bans)
