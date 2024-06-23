from typing import Self

from django.db import models
from django.utils import timezone

__all__ = [
    "SoftDeleteQuerySet",
]


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(deleted_at=timezone.now())
        return True, self.count()

    def restore(self):
        self.update(deleted_at=None)
        return True, self.count()

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()

    def filter(self, *args, **kwargs) -> Self:
        return super(SoftDeleteQuerySet, self).filter(*args, **kwargs)
