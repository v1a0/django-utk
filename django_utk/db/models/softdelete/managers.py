from django.db import models

from django_utk.db.models.softdelete.querysets import SoftDeleteQuerySet


__all__ = [
    "SoftDeleteManager",
]


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(
            deleted_at__isnull=True
        )
