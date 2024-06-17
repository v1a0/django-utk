from typing import Type, Union

from django.db import models
from django.db.models.options import Options


def get_model_meta(model: Union[Type[models.Model], models.Model]) -> Options:
    return getattr(model, "_meta", getattr(model, "Meta"))
