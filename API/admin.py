from django.contrib import admin
from API.models import APIKey, APIRequests, APIPermissions, APIKeys_Permissions

# API
admin.site.register(APIKey)
admin.site.register(APIRequests)
admin.site.register(APIPermissions)
admin.site.register(APIKeys_Permissions)
