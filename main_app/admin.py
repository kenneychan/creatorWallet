from django.contrib import admin
# import your models here
from .models import Deal, Platform, Attachment, Activity
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class DealResource(resources.ModelResource):
   class Meta:
      model = Deal
class DealAdmin(ImportExportModelAdmin):
   resource_class = DealResource

class PlatformResource(resources.ModelResource):
   class Meta:
      model = Platform
class PlatformAdmin(ImportExportModelAdmin):
   resource_class = PlatformResource

class AttachmentResource(resources.ModelResource):
   class Meta:
      model = Attachment
class AttachmentAdmin(ImportExportModelAdmin):
   resource_class = AttachmentResource

class ActivityResource(resources.ModelResource):
   class Meta:
      model = Activity
class ActivityAdmin(ImportExportModelAdmin):
   resource_class = ActivityResource

# Register your models here.
admin.site.register(Deal,DealAdmin)
admin.site.register(Platform,PlatformAdmin)
admin.site.register(Attachment,AttachmentAdmin)
admin.site.register(Activity,ActivityAdmin)