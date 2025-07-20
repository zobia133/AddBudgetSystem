from celery import shared_task
from django.utils import timezone
from .models import Budget, Campaign
from datetime import timedelta

@shared_task
def reset_daily_spends():
    today = timezone.localdate()
    for budget in Budget.objects.all():
        if budget.last_daily_reset < today:
            budget.spend_to_date_daily = 0
            budget.last_daily_reset = today
            budget.save()
            # Reactivate campaigns if they were paused by daily budget
            for campaign in budget.campaigns.filter(is_paused_by_budget=True):
                if budget.spend_to_date_daily < budget.daily_limit and budget.spend_to_date_monthly < budget.monthly_limit:
                    campaign.is_active = True
                    campaign.is_paused_by_budget = False
                    campaign.save()

@shared_task
def reset_monthly_spends():
    now = timezone.now()
    first_of_month = now.replace(day=1).date()
    for budget in Budget.objects.all():
        if budget.last_monthly_reset < first_of_month:
            budget.spend_to_date_monthly = 0
            budget.last_monthly_reset = first_of_month
            budget.save()
            # Reactivate campaigns if they were paused by monthly budget
            for campaign in budget.campaigns.filter(is_paused_by_budget=True):
                if budget.spend_to_date_daily < budget.daily_limit and budget.spend_to_date_monthly < budget.monthly_limit:
                    campaign.is_active = True
                    campaign.is_paused_by_budget = False
                    campaign.save()

@shared_task
def check_and_enforce_budgets():
    for budget in Budget.objects.all():
        over_daily = budget.spend_to_date_daily >= budget.daily_limit
        over_monthly = budget.spend_to_date_monthly >= budget.monthly_limit
        for campaign in budget.campaigns.all():
            if (over_daily or over_monthly) and campaign.is_active:
                campaign.is_active = False
                campaign.is_paused_by_budget = True
                campaign.save()
            elif not (over_daily or over_monthly) and campaign.is_paused_by_budget:
                campaign.is_active = True
                campaign.is_paused_by_budget = False
                campaign.save()

@shared_task
def enforce_dayparting():
    now = timezone.localtime()
    day = now.strftime("%a")  # e.g., 'Mon'
    time_now = now.time()
    for budget in Budget.objects.all():
        dayparts = budget.dayparts.all()
        in_daypart = False
        for dp in dayparts:
            days = [d.strip() for d in dp.days_of_week.split(",")]
            if day in days and dp.start_time <= time_now <= dp.end_time:
                in_daypart = True
                break
        for campaign in budget.campaigns.all():
            if in_daypart and campaign.is_paused_by_daypart:
                campaign.is_active = True
                campaign.is_paused_by_daypart = False
                campaign.save()
            elif not in_daypart and campaign.is_active:
                campaign.is_active = False
                campaign.is_paused_by_daypart = True
                campaign.save()