from typing import TypedDict, Optional, List
from .models import Campaign

class CampaignData(TypedDict):
    id: int
    name: str

def get_active_campaigns() -> List[CampaignData]:
    return [
        {"id": c.id, "name": c.name}
        for c in Campaign.objects.filter(active=True)
    ]