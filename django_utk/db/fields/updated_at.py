from django.db import models


__all__ = [
    "UpdatedAtField",
]


class UpdatedAtField(models.DateTimeField):

    _required_kwargs = {
        "auto_now": True,
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(self._required_kwargs)
        models.DateTimeField.__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.update(self._required_kwargs)
        return name, path, args, kwargs
