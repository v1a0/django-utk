from typing import Type

from django.db import models


__all__ = [
    "BaseManager",
    "Manager"
]


class BaseManager:
    queryset_class: Type[models.QuerySet] = models.QuerySet

    def get_queryset(self) -> queryset_class:
        return self.queryset_class(self.model, using=self._db)


class Manager(BaseManager, models.Manager):
    pass

