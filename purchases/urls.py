from django.urls import path, include

from rest_framework import routers

from purchases.views import PurchaseAPIView


router = routers.SimpleRouter()
router.register('purchases', PurchaseAPIView, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
]
