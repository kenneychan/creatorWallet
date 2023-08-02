from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Deal, PlatformContent
from .forms import DealForm, PlatformForm

def deals_form(request):
  return {'DealForm': DealForm()}

def platforms_form(request):
  return {'PlatformForm': PlatformForm()}