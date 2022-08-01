from django.db import models

from purchases.logic import update_monthly_costs


class MonthlyCosts(models.Model):

    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    total = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.month}/{self.year}"

    class Meta:
        ordering = ["-year", "-month"]
        verbose_name_plural = "MonthlyCosts"


class Purchase(models.Model):

    name = models.CharField(max_length=255)
    cost = models.PositiveIntegerField()
    date = models.DateField(db_index=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        res = super().save(*args, **kwargs)

        self.refresh_from_db()
        update_monthly_costs(purchase=self)

        return res

    class Meta:
        ordering = ["-date"]
