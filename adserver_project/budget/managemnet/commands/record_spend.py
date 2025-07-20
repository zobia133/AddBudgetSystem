from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from ...models import Campaign, SpendEvent

class Command(BaseCommand):
    help = 'Record spend for a campaign (simulate ad delivery)'

    def add_arguments(self, parser):
        parser.add_argument('campaign_id', type=int)
        parser.add_argument('amount', type=str)

    def handle(self, *args, **kwargs):
        campaign_id = kwargs['campaign_id']
        amount = Decimal(kwargs['amount'])
        campaign = Campaign.objects.get(id=campaign_id)
        budget = campaign.budget

        # Check for daypart
        now = timezone.localtime()
        day = now.strftime("%a")
        in_daypart = False
        for dp in budget.dayparts.all():
            days = [d.strip() for d in dp.days_of_week.split(",")]
            if day in days and dp.start_time <= now.time() <= dp.end_time:
                in_daypart = True
                break
        if not in_daypart:
            self.stdout.write(self.style.ERROR(f'Campaign {campaign.name} is outside active daypart.'))
            return

        # Check budget limits
        if budget.spend_to_date_daily + amount > budget.daily_limit:
            campaign.is_active = False
            campaign.is_paused_by_budget = True
            campaign.save()
            self.stdout.write(self.style.ERROR(f'Daily budget exceeded. Pausing campaign {campaign.name}.'))
            return
        if budget.spend_to_date_monthly + amount > budget.monthly_limit:
            campaign.is_active = False
            campaign.is_paused_by_budget = True
            campaign.save()
            self.stdout.write(self.style.ERROR(f'Monthly budget exceeded. Pausing campaign {campaign.name}.'))
            return

        # Record spend
        SpendEvent.objects.create(campaign=campaign, amount=amount)
        budget.spend_to_date_daily += amount
        budget.spend_to_date_monthly += amount
        budget.save()
        self.stdout.write(self.style.SUCCESS(f'Spend of {amount} recorded for campaign {campaign.name}.'))