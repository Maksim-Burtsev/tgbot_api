from rest_framework import generics, viewsets

from purchases.models import Purchase
from purchases.serializers import PurchaseSerializer


class PurchaseAPIView(viewsets.ModelViewSet):
    
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return Purchase.objects.all()

    #TODO filters