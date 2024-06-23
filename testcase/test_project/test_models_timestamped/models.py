from django.db import models

from django_utk.db.models import TimeStampedModel
from django_utk.db.models.timestamped import CreatedAtField, UpdatedAtField


class TimeStampedNote(TimeStampedModel):
    """
    Just regular note with text and timestamps
    """

    created_at: CreatedAtField
    updated_at: UpdatedAtField

    text = models.TextField()
