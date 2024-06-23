from typing import Iterable

from django.db import models
from django.utils import timezone

__all__ = [
    "TimeStampedQuerySet",
]


def set_timestamp_for_each(items: Iterable, attrs: list[str]):
    now = timezone.now()

    for attr in attrs:
        for item in items:
            setattr(item, attr, now)

    return items


class TimeStampedQuerySet(models.QuerySet):
    _created_at_attr = "created_at"
    _updated_at_attr = "updated_at"

    def create(self, *, skip_timestamping=False, **kwargs):
        if not skip_timestamping:
            kwargs[self._created_at_attr] = kwargs[self._updated_at_attr] = (
                timezone.now()
            )

        return super().create(**kwargs)

    def update(self, *, skip_timestamping=False, **kwargs):
        if not skip_timestamping:
            kwargs[self._updated_at_attr] = timezone.now()

        return super().update(**kwargs)

    def bulk_create(self, objs, *args, skip_timestamping=False, **kwargs):
        if not skip_timestamping:
            set_timestamp_for_each(objs, [self._created_at_attr, self._updated_at_attr])

        return super().bulk_create(objs, *args, **kwargs)

    def abulk_create(self, objs, *args, skip_timestamping=False, **kwargs):
        if not skip_timestamping:
            set_timestamp_for_each(objs, [self._created_at_attr, self._updated_at_attr])

        return super().abulk_create(objs, *args, **kwargs)

    def bulk_update(self, objs, *args, skip_timestamping=False, **kwargs):
        if not skip_timestamping:
            set_timestamp_for_each(objs, [self._updated_at_attr])

        return super().bulk_update(objs, *args, **kwargs)

    def abulk_update(self, objs, *args, skip_timestamping=False, **kwargs):
        if not skip_timestamping:
            set_timestamp_for_each(objs, [self._updated_at_attr])

        return super().abulk_update(objs, *args, **kwargs)
