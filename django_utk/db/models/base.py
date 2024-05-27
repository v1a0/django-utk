from django.db import models

from django_utk.db.models.meta import ABCModelMeta

__all__ = [
    "BaseModelMixin",
]


class BaseModelMixin(models.Model, metaclass=ABCModelMeta):
    """
    Base ModelMixin
    """

    class Meta:
        abstract = True
