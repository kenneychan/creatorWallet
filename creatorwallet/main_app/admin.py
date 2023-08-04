from django.contrib import admin
# import your models here
from .models import Deal, Platform, Attachment, Activity

# Register your models here.
admin.site.register(Deal)
admin.site.register(Platform)
admin.site.register(Attachment)
admin.site.register(Activity)