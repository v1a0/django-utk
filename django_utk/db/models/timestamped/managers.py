from django.db import models

from common.abc import ABCManager
from django_utk.db.models.timestamped.querysets import TimeStampedQuerySet


class BaseTimeStampedManager(ABCManager):
    QuerySetClass = TimeStampedQuerySet


class TimeStampedManager(BaseTimeStampedManager, models.Manager):
    pass
