from django.contrib import admin
# import your models here
# from .models import Cat
from .models import Deal
from .models import Attachment

# Register your models here.
admin.site.register(Deal)
admin.site.register(Attachment)