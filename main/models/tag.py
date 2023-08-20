from django.db import models


class Tag(models.Model):
    header = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.header
