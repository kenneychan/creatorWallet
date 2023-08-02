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
  path('deals/<int:deal_id>/assoc_platformContent/<int:platformContent_id>/', views.assoc_platformContent, name='assoc_platformContent'),
  path('deals/<int:deal_id>/unassoc_platformContent/<int:platformContent_id>/', views.unassoc_platformContent, name='unassoc_platform'),
  path('platformsContent/', views.PlatformContentList.as_view(), name='platformsContent_index'),
  path('platformsContent/<int:pk>/', views.PlatformContentDetail.as_view(), name='platformsContent_detail'),
  path('platformsContent/create/', views.PlatformContentCreate.as_view(), name='platformsContent_create'),
  path('platformsContent/<int:pk>/update/', views.PlatformContentUpdate.as_view(), name='platformsContent_update'),
  path('platformsContent/<int:pk>/delete/', views.PlatformContentDelete.as_view(), name='platformsContent_delete'),
]