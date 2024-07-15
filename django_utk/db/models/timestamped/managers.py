from django.db import models

import django_utk.db.models as utk_models
from django_utk.db.models.timestamped.querysets import TimeStampedQuerySet


class BaseTimeStampedManager(utk_models.BaseManager):
    queryset_class = TimeStampedQuerySet


class TimeStampedManager(BaseTimeStampedManager, models.Manager):
    pass
