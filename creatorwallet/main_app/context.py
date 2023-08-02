from .forms import DealForm

def deals_form(request):
  return {'DealForm': DealForm()}