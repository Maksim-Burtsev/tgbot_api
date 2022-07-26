from django.utils import timezone
from django.db import models


class Note(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        if self.category:
            self.category = self.category.lower()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
