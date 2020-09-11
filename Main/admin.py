from django.contrib import admin
import Main.models as models


admin.site.register(models.Articles)
admin.site.register(models.UserData)
admin.site.register(models.Bans)
