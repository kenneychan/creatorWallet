from django.forms import ModelForm
from .models import Deal, Platform, Activity

class DealForm(ModelForm):
  class Meta:
    model = Deal
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']

class PlatformForm(ModelForm):
  class Meta:
    model = Platform
    fields = ['name', 'url', 'platform_username']
    
class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    fields = ['activity', 'date', 'notes']
    
