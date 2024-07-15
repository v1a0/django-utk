from django.db import connection, models

from django_utk.db.models.utils import get_model_meta as meta

__all__ = [
    "MaterializedDBViewModelMixin",
]


class MaterializedDBViewModelMixin(models.Model):
    @classmethod
    def refresh(cls):
        with connection.cursor() as cursor:
            cursor.execute(f"REFRESH MATERIALIZED VIEW {meta(cls).db_table};")

    class Meta:
        abstract = True
