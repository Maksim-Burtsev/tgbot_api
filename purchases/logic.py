from django.apps import apps
from django.db.models import F


def update_monthly_costs(purchase) -> None:
    """Update total of MonthlyCosts"""

    MonthlyCosts = apps.get_model("purchases.MonthlyCosts")

    monthly, created = MonthlyCosts.objects.get_or_create(
        month=purchase.date.month, year=purchase.date.year
    )

    if created:
        monthly.total = purchase.cost
    else:
        monthly.total = F("total") + purchase.cost

    monthly.save()
