from django.forms import ModelForm
from .models import Deal, PlatformContent, Activity

class DealForm(ModelForm):
  class Meta:
    model = Deal
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']

class PlatformForm(ModelForm):
  class Meta:
    model = PlatformContent
    fields = ['name', 'url']
    
class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    fields = ['activity', 'date', 'notes']
    
