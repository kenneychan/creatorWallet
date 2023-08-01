from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  # New url pattern below
  path('accounts/signup/', views.signup, name='signup'),
  path('deals/', views.deals_index, name='index'),
  path('deals/<int:deal_id>/', views.deals_detail, name='detail'),
  path('deals/create/', views.DealCreate.as_view(), name='deals_create'),
  path('deals/<int:pk>/update/', views.DealUpdate.as_view(), name='deals_update'),
  path('deals/<int:pk>/delete/', views.DealDelete.as_view(), name='deals_delete'),
  path('deals/<int:deal_id>/add_attachment/', views.add_attachment, name='add_attachment'),
]