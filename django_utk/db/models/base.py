from django.db import models

from django_utk.db.models.meta import ABCModelMeta

__all__ = [
    "ABCModel",
    "ModelMixin",
]


class ABCModel(models.Model, metaclass=ABCModelMeta):
    class Meta:
        abstract = True


class ModelMixin(models.Model):
    class Meta:
        abstract = True
