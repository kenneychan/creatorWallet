from django.contrib import admin
# import your models here
from .models import Deal, PlatformContent, Attachment

# Register your models here.
admin.site.register(Deal)
admin.site.register(PlatformContent)
admin.site.register(Attachment)