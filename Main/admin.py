from django.contrib import admin
from Main.models import Articles, Views, Rating, Comments, CommentsRating, Reports, ReportTypes
from Users.models import Profile, Bans

# Main
admin.site.register(Articles)
admin.site.register(Views)
admin.site.register(Rating)
admin.site.register(Comments)
admin.site.register(CommentsRating)
admin.site.register(ReportTypes)
admin.site.register(Reports)

# Users
admin.site.register(Profile)
admin.site.register(Bans)
