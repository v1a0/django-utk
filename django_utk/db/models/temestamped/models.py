from django.db import models

from django_utk.db.fields import CreatedAtField, UpdatedAtField


__all__ = [
    "TimeStampedModel",
]


class TimeStampedModel(models.Model):

    created_at = CreatedAtField()
    updated_at = UpdatedAtField()

    class Meta:
        abstract = True
