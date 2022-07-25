from django.db import models


class Purchase(models.Model):

    name = models.CharField(max_length=255)
    cost = models.PositiveIntegerField()
    date = models.DateField(db_index=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-date']


class MonthlyCosts(models.Model):

    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    total = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'{self.month}/{self.year}'

    class Meta:
        ordering = ['-year', '-month']
        verbose_name_plural = 'MonthlyCosts'

