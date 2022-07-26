from django_filters import rest_framework as filters

from purchases.models import Purchase


class PurchasesFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    from_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Purchase
        fields = ("cost", )


class PurchasesDateFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Purchase
        fields = ()


class MonthYearFilter(filters.FilterSet):
    month = filters.NumberFilter()
    year = filters.DateFilter()
