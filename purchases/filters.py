from django_filters import rest_framework as filters

from purchases.models import Purchase


class PurchasesFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="date", lookup_expr="lte")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Purchase
        fields = ("name", "cost")


class PurchasesDateFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Purchase
        fields = ()
