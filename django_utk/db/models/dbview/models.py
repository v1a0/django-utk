from django.db import models

from django_utk.db.models import fix
from django_utk.db.models.dbview import DBViewManager
from django_utk.db.models.dbview.mixins import MaterializedDBViewModelMixin

__all__ = [
    "DBViewModel",
    "MaterializedDBViewModel",
]


class DBViewModel(fix.DeleteUsingManager, models.Model):
    objects = DBViewManager()

    class Meta:
        abstract = True
        managed = False
        db_table = NotImplemented


class MaterializedDBViewModel(MaterializedDBViewModelMixin, DBViewModel):
    objects: DBViewManager  # DBViewModel

    class Meta:
        abstract = True
        managed = False
        db_table = NotImplemented
