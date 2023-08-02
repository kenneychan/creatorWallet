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
  path('deals/<int:deal_id>/assoc_platform_content/<int:platform_content_id>/', views.assoc_platform_content, name='assoc_platform_content'),
  path('deals/<int:deal_id>/unassoc_platform_content/<int:platform_content_id>/', views.unassoc_platform_content, name='unassoc_platform'),
  path('platforms_content/', views.Platform_contentList.as_view(), name='platforms_content_index'),
  path('platforms_content/<int:pk>/', views.Platform_contentDetail.as_view(), name='platforms_content_detail'),
  path('platforms_content/create/', views.Platform_contentCreate.as_view(), name='platforms_content_create'),
  path('platforms_content/<int:pk>/update/', views.Platform_contentUpdate.as_view(), name='platforms_content_update'),
  path('platforms_content/<int:pk>/delete/', views.Platform_contentDelete.as_view(), name='platforms_content_delete'),
]