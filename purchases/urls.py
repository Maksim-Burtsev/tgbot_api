from django.urls import path, include

from rest_framework import routers

from purchases.views import (
    PurchaseAPIView, 
    PurchasesListAPIView,
    MonthlyCostsView
)


router = routers.SimpleRouter()
router.register("purchases", PurchaseAPIView, basename="purchases")

urlpatterns = [
    path("", include(router.urls)),
    path("get_purchases/", PurchasesListAPIView.as_view()),
    path("get_monthly_costs/", MonthlyCostsView.as_view()),
]
