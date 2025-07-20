from django.urls import path
from . import views

urlpatterns = [
    # Advertiser URLs
    path('advertisers/', views.AdvertiserListView.as_view(), name='advertiser_list'),
    path('advertiser/add/', views.AdvertiserCreateView.as_view(), name='advertiser_add'),
    path('advertiser/<int:pk>/', views.AdvertiserDetailView.as_view(), name='advertiser_detail'),

    # Budget URLs
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budget/add/', views.BudgetCreateView.as_view(), name='budget_add'),
    path('budget/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),

    # Campaign URLs
    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaign/add/', views.CampaignCreateView.as_view(), name='campaign_add'),
    path('campaign/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaign/<int:pk>/toggle/', views.toggle_campaign_status, name='toggle_campaign_status'),

    # Daypart URLs
    path('dayparts/', views.DaypartListView.as_view(), name='daypart_list'),
    path('daypart/add/', views.DaypartCreateView.as_view(), name='daypart_add'),
    path('daypart/<int:pk>/', views.DaypartDetailView.as_view(), name='daypart_detail'),

    # SpendEvent URLs
    path('spendevents/', views.SpendEventListView.as_view(), name='spendevent_list'),
    path('spendevent/add/', views.SpendEventCreateView.as_view(), name='spendevent_add'),
    path('spendevent/<int:pk>/', views.SpendEventDetailView.as_view(), name='spendevent_detail'),
]