from rest_framework import viewsets

from django_filters import rest_framework as filters

from purchases.models import Purchase
from purchases.serializers import PurchaseSerializer
from purchases.filters import PurchasesFilter


class PurchaseAPIView(viewsets.ModelViewSet):
    """CRUD for Purchases"""

    serializer_class = PurchaseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PurchasesFilter

    def get_queryset(self):
        return Purchase.objects.all()

    # TODO create list obj
