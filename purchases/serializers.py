from rest_framework import serializers

from purchases.models import Purchase


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ("id", "name", "cost", "date")


class PurchaseWithTotalCount(serializers.ModelSerializer):
    total = serializers.IntegerField(read_only=True)
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Purchase
        fields = ("name", "total", "count")
