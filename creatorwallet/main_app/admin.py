from django.contrib import admin
# import your models here
from .models import Deal, PlatformContent

# Register your models here.
admin.site.register(Deal)
admin.site.register(PlatformContent)