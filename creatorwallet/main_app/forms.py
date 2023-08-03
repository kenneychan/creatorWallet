from django.forms import ModelForm
from .models import Deal, Activity

class DealForm(ModelForm):
  class Meta:
    model = Deal
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']

class ActivityForm(ModelForm):
  class Meta:
    model = Activity
    fields = ['date', 'notes', 'deal']