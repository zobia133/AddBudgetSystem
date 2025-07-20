from django.contrib import admin
from .models import Advertiser, Budget, Campaign, Daypart, SpendEvent

admin.site.register(Advertiser)
admin.site.register(Budget)
admin.site.register(Campaign)
admin.site.register(Daypart)
admin.site.register(SpendEvent)
