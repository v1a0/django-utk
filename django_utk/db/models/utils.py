import functools
from typing import Type, Union

from django.db import models
from django.db.models.options import Options


def get_model_meta(model: Union[Type[models.Model], models.Model]) -> Options:
    return getattr(model, "_meta", getattr(model, "Meta"))


@functools.lru_cache()
def get_model_fields(model: Type[models.Model]):
    return {field.name: field for field in model._meta.fields}
