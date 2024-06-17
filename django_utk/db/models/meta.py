import abc

from django.db import models


class ABCModelMeta(abc.ABCMeta, type(models.Model)):
    """
    Absolute accurate meta-class for django model
    """
