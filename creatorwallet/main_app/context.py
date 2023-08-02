from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Deal
from .forms import DealForm

def deals_form(request):
  return {'DealForm': DealForm()}

@login_required
def deals_delete_form(request):
  deals = Deal.objects.filter(user=request.user)

  return render(request, 'deals/index.html', { 'deals': deals })