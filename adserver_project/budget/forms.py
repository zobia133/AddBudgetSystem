from django import forms
from .models import Advertiser, Budget, Campaign, Daypart, SpendEvent

class AdvertiserForm(forms.ModelForm):
    class Meta:
        model = Advertiser
        fields = ['name']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['advertiser', 'daily_limit', 'monthly_limit']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['budget', 'name', 'is_active']

class DaypartForm(forms.ModelForm):
    class Meta:
        model = Daypart
        fields = ['budget', 'start_time', 'end_time', 'days_of_week']

class SpendEventForm(forms.ModelForm):
    class Meta:
        model = SpendEvent
        fields = ['campaign', 'amount']