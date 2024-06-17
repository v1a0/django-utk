from django.db import models

from django_utk.db.fields import CreatedAtField, UpdatedAtField
from django.utils.translation import gettext_lazy as _


__all__ = [
    "TimeStampedModel",
]


class TimeStampedModel(models.Model):

    created_at = CreatedAtField(_("Created at"))
    updated_at = UpdatedAtField(_("Updated at"))

    class Meta:
        abstract = True
