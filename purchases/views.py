from django.db.models import Sum, Count

from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, viewsets

from django_filters import rest_framework as filters

from purchases.models import Purchase, MonthlyCosts
from purchases.serializers import (
    PurchaseSerializer,
    PurchaseWithTotalCount,
    MontlyCostsSerializer,
)
from purchases.filters import PurchasesFilter, PurchasesDateFilter, MonthYearFilter


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


class MonthlyCostsView(views.APIView):

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MonthYearFilter

    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if month and year:
            data = MonthlyCosts.objects.filter(month=month, year=year).values()
            data = data[0] if len(data) > 0 else []

            serializer = MontlyCostsSerializer(data=data)
            serializer.is_valid()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(
            data={"detail": "month and year - required params"},
            status=status.HTTP_400_BAD_REQUEST,
        )
