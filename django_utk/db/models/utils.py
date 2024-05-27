from typing import Type

from django.db import models
from django.db.models.options import Options


def get_model_meta(model: Type[models.Model]) -> Options:
    return getattr(model, "_meta")
