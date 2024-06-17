from django.db import models

from django_utk.db.fields import CreatedAtField, UpdatedAtField
from django_utk.db.models import TimeStampedModel


class TimeStampedNote(TimeStampedModel):
    """
    Just regular note with text and timestamps
    """

    created_at: CreatedAtField
    updated_at: UpdatedAtField

    text = models.TextField()
