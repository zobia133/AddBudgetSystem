from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Advertiser, Budget, Campaign, Daypart, SpendEvent
from .forms import AdvertiserForm, BudgetForm, CampaignForm, DaypartForm, SpendEventForm

# Advertiser Views
class AdvertiserListView(ListView):
    model = Advertiser

class AdvertiserCreateView(CreateView):
    model = Advertiser
    form_class = AdvertiserForm
    success_url = reverse_lazy('advertiser_list')

class AdvertiserDetailView(DetailView):
    model = Advertiser

# Budget Views
class BudgetListView(ListView):
    model = Budget

class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    success_url = reverse_lazy('budget_list')

class BudgetDetailView(DetailView):
    model = Budget

# Campaign Views
class CampaignListView(ListView):
    model = Campaign

class CampaignCreateView(CreateView):
    model = Campaign
    form_class = CampaignForm
    success_url = reverse_lazy('campaign_list')

class CampaignDetailView(DetailView):
    model = Campaign

def toggle_campaign_status(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    campaign.is_active = not campaign.is_active
    campaign.save()
    return redirect('campaign_detail', pk=pk)

# Daypart Views
class DaypartListView(ListView):
    model = Daypart

class DaypartCreateView(CreateView):
    model = Daypart
    form_class = DaypartForm
    success_url = reverse_lazy('daypart_list')

class DaypartDetailView(DetailView):
    model = Daypart

# SpendEvent Views
class SpendEventListView(ListView):
    model = SpendEvent

class SpendEventCreateView(CreateView):
    model = SpendEvent
    form_class = SpendEventForm
    success_url = reverse_lazy('spendevent_list')

class SpendEventDetailView(DetailView):
    model = SpendEvent