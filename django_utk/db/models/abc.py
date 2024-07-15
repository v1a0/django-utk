import abc

from django.db import models

__all__ = [
    "ABCModel",
    "ABCModelMeta",
]


class ABCModelMeta(abc.ABCMeta, type(models.Model)):
    """
    Absolute accurate meta-class for django model
    """


class ABCModel(models.Model, metaclass=ABCModelMeta):
    class Meta:
        abstract = True
