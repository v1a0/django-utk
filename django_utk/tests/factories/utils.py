import functools
from typing import Type

from django.db import models


@functools.lru_cache()
def get_model_fields(model: Type[models.Model]):
    return {field.name: field for field in model._meta.fields}
