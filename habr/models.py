from django.db import models


class Post(models.Model):

    url = models.URLField(unique=True)

    def __str__(self) -> str:
        return self.url