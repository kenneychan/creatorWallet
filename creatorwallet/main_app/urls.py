from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  # New url pattern below
  path('accounts/signup/', views.signup, name='signup'),
  path('deals/', views.deals_index, name='index'),
]