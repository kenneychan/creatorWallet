from django.forms import ModelForm
from .models import Deal

class DealForm(ModelForm):
  class Meta:
    model = Deal
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']

