from django.contrib import admin
# import your models here
from .models import Deal, Platform_content

# Register your models here.
admin.site.register(Deal)
admin.site.register(Platform_content)