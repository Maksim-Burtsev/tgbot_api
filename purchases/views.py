from django.db.models import Sum, Count

from rest_framework import generics, viewsets
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework import status
from rest_framework.response import Response

from django_filters import rest_framework as filters

from purchases.models import Purchase
from purchases.serializers import PurchaseSerializer, PurchaseWithTotalCount
from purchases.filters import PurchasesFilter, PurchasesDateFilter


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

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PurchasesListAPIView(generics.ListAPIView):

    serializer_class = PurchaseWithTotalCount
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PurchasesDateFilter

    def get_queryset(self):
        return (
            Purchase.objects.values("name")
            .annotate(total=Sum("cost"), count=Count("name"))
            .order_by("-total")
        )
