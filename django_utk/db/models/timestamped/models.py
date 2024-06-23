from django.db import models
from django.utils.translation import gettext_lazy as _

from django_utk.db.models.timestamped.fields import CreatedAtField, UpdatedAtField
from django_utk.db.models.timestamped.managers import TimeStampedManager

__all__ = [
    "TimeStampedModel",
]


class TimeStampedModel(models.Model):
    """
    A TimeStampedModel model automatically records the time when an object
    is created (`created_at`) and updated (`updated_at`). This is useful
    for keeping track of when records are added or modified in the
    database, providing crucial information for auditing, analytics,
    and debugging purposes.

    Attributes:
        created_at (CreatedAtField): DateTimeField indicating the timestamp when
            the object was created.
        updated_at (UpdatedAtField): DateTimeField indicating the timestamp of
            the last update to the object.

    Manager:
        objects (TimeStampedManager): Automatically updates the `created_at`
            and `updated_at` fields on object creation and modification.
    """

    created_at = CreatedAtField(_("Created at"))
    updated_at = UpdatedAtField(_("Updated at"))

    objects = TimeStampedManager()

    class Meta:
        abstract = True
