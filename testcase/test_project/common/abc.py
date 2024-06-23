from abc import ABC
from typing import Type

from django.db import models


class ABCManager(ABC):
    QuerySetClass: Type[models.QuerySet] = NotImplemented

    def get_queryset(self) -> QuerySetClass:
        return self.QuerySetClass(self.model, using=self._db)
