from django.db import models
from django.utils import timezone

class Advertiser(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Budget(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE, related_name="budgets")
    daily_limit = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_limit = models.DecimalField(max_digits=12, decimal_places=2)
    spend_to_date_daily = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    spend_to_date_monthly = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_daily_reset = models.DateField(default=timezone.now)
    last_monthly_reset = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Budget for {self.advertiser.name}"

class Campaign(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="campaigns")
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_paused_by_budget = models.BooleanField(default=False)
    is_paused_by_daypart = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Daypart(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="dayparts")
    start_time = models.TimeField()
    end_time = models.TimeField()
    days_of_week = models.CharField(max_length=20)  # e.g. "Mon,Tue,Wed"

    def __str__(self):
        return f"{self.budget} {self.start_time}-{self.end_time} {self.days_of_week}"
def get_campaign_count(self) -> int:
        return self.campaign_set.count()
class SpendEvent(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="spend_events")
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
  