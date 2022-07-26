from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

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

    def create(self, request, *args, **kwargs):
        
        is_many = isinstance(request.data, list)

        if not is_many:
            return super().create(request, *args, **kwargs)
        
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

