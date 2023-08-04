from django.urls import path
from . import views, context

urlpatterns = [
  path('', views.home, name='home'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('about/', views.about, name='about'),
  # New url pattern below
  path('accounts/signup/', views.signup, name='signup'),
  path('deals/', views.deals_index, name='index'),
  path('deals/<int:deal_id>/', views.deals_detail, name='detail'),
  path('deals/create/', views.DealCreate.as_view(), name='deals_create'),
  path('deals/<int:pk>/update/', views.DealUpdate.as_view(), name='deals_update'),
  path('deals/<int:pk>/delete/', views.DealDelete.as_view(), name='deals_delete'),
  path('deals/<int:deal_id>/assoc_platform/<int:platform_id>/', views.assoc_platform, name='assoc_platform'),
  path('deals/<int:deal_id>/unassoc_platform/<int:platform_id>/', views.unassoc_platform, name='unassoc_platform'),
  path('platforms/', views.PlatformList.as_view(), name='platforms_index'),
  path('platforms/<int:platform_id>/', views.platforms_detail, name='platforms_detail'),
  path('platforms/create/', views.PlatformCreate.as_view(), name='platforms_create'),
  path('platforms/<int:pk>/update/', views.PlatformUpdate.as_view(), name='platforms_update'),
  path('platforms/<int:pk>/delete/', views.PlatformDelete.as_view(), name='platforms_delete'),
  path('deals/<int:deal_id>/add_attachment/', views.add_attachment, name='add_attachment'),
  path('deals/<int:deal_id>/delete_attachment/<int:attachment_id>/', views.delete_attachment, name='delete_attachment'),
  path('deals/<int:deal_id>/add_activity/', views.add_activity, name='add_activity'),
  path('platforms/<int:pk>/update/', context.platforms_form, name='platforms_form'),
  path('deals/<int:pk>/update/', context.deals_form, name='deals_form'),
]