from django.db import models

__all__ = [
    "CreatedAtField",
    "UpdatedAtField",
]


class CreatedAtField(models.DateTimeField):
    """
    Unified 'created_at' field for timestamped models

    Have preset automatic filling by current datetime on instance creation
    and readonly mode for admin panel
    """

    _required_kwargs = {
        "auto_now_add": True,
        "blank": True,
        "editable": False,
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(self._required_kwargs)
        models.DateTimeField.__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.update(self._required_kwargs)
        return name, path, args, kwargs


class UpdatedAtField(models.DateTimeField):
    """
    Unified 'created_at' field for timestamped models

    Have preset automatic filling by current datetime on instance update
    and readonly mode for admin panel
    """

    _required_kwargs = {
        "auto_now": True,
        "blank": True,
        "editable": False,
    }

    def __init__(self, *args, **kwargs):
        kwargs.update(self._required_kwargs)
        models.DateTimeField.__init__(self, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs.update(self._required_kwargs)
        return name, path, args, kwargs
