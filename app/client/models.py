from django.db import models

from core.models import AuditableModel


# Create your models here.
class Client(AuditableModel):
    name = models.CharField(max_length=50, db_index=True)
    key = models.CharField(max_length=50, db_index=True, unique=True)

    class Meta:
        ordering = ("created_at",)