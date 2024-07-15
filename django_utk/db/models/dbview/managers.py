from django.db import models

import django_utk.db.models as utk_models

from django_utk.db.models.dbview.querysets import DBViewQuerySet

__all__ = [
    "DBViewManager",
]


class BaseDBViewManager(utk_models.BaseManager):
    queryset_class = DBViewQuerySet


class DBViewManager(BaseDBViewManager, models.Manager):
    pass
