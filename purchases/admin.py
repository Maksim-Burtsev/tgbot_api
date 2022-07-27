from django.contrib import admin

from purchases.models import Purchase, MonthlyCosts


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'date')


@admin.register(MonthlyCosts)
class MonthlyCostsAdmin(admin.ModelAdmin):
    list_display = ('get_month_with_year', 'total')

    def get_month_with_year(self, obj):
        return f"{obj.month}/{obj.year}"