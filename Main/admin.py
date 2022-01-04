from django.contrib import admin
from Main.models import Articles, Views, Rating, Comments, CommentsRating
from Users.models import Profile, Bans

# Main
admin.site.register(Articles)
admin.site.register(Views)
admin.site.register(Rating)
admin.site.register(Comments)
admin.site.register(CommentsRating)

# Users
admin.site.register(Profile)
admin.site.register(Bans)
