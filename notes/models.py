from django.db import models
from django.utils import timezone


class Note(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now())
    category = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
