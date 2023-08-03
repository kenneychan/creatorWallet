from django.urls import path
from . import views, context

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
  path('deals/<int:deal_id>/assoc_platformcontent/<int:platformcontent_id>/', views.assoc_platformcontent, name='assoc_platformcontent'),
  path('deals/<int:deal_id>/unassoc_platformcontent/<int:platformcontent_id>/', views.unassoc_platformcontent, name='unassoc_platformcontent'),
  path('platformscontent/', views.PlatformContentList.as_view(), name='platformscontent_index'),
  
  path('platformscontent/<int:platformcontent_id>/', views.platformContents_detail, name='platformscontent_detail'),
  
  path('platformscontent/create/', views.PlatformContentCreate.as_view(), name='platformscontent_create'),
  path('platformscontent/<int:pk>/update/', views.PlatformContentUpdate.as_view(), name='platformscontent_update'),
  path('platformscontent/<int:pk>/delete/', views.PlatformContentDelete.as_view(), name='platformscontent_delete'),
  path('deals/<int:deal_id>/add_attachment/', views.add_attachment, name='add_attachment'),
  path('deals/<int:deal_id>/add_activity/', views.add_activity, name='add_activity'),
  path('platformscontent/<int:pk>/update/', context.platforms_form, name='platforms_form'),
  path('deals/<int:pk>/update/', context.deals_form, name='deals_form'),
]