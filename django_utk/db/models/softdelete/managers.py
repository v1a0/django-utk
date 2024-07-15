
from django.db import models

import django_utk.db.models as utk_models
from django_utk.db.models.softdelete.querysets import SoftDeleteQuerySet

__all__ = [
    "BaseSoftDeleteManager",
    "SoftDeleteManager",
]


class BaseSoftDeleteManager(utk_models.BaseManager):
    QuerySetClass = SoftDeleteQuerySet

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteManager(BaseSoftDeleteManager, models.Manager):
    pass
