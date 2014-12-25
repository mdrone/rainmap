from apps.rainmap.models import Scan, Blacklist, UserProfile
from django.contrib import admin

# Register your models here.

admin.site.register(Scan)
admin.site.register(Blacklist)
admin.site.register(UserProfile)
