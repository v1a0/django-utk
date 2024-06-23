from django.db import models

from django_utk.db.models.dbview import DBViewQuerySet

__all__ = [
    "DBViewManager",
]

DBViewManager = models.Manager.from_queryset(DBViewQuerySet, class_name="DBViewManager")
