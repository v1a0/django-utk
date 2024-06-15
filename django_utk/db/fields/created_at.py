from django.db import models
from django.utils.translation import gettext_lazy as _


__all__ = [
    "CreatedAtField",
]


class CreatedAtField(models.DateTimeField):

    _required_kwargs = {
        "auto_now_add": True,
        "blank": True,
        "editable": False,
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(self._required_kwargs)
        super().__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.update(self._required_kwargs)
        return name, path, args, kwargs
