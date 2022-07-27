from django.db import models
from django.db.models import F


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
        self.name = self.name.title()
        
        monthly, created = MonthlyCosts.objects.get_or_create(month=self.date.month, year=self.date.year)
        
        if created:
            monthly.total = self.cost
        else:
            monthly.total = F('total') + self.cost

        monthly.save()

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]
