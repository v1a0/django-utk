from django_utk.utils.env import PYTHON_VERSION
if PYTHON_VERSION >= (3, 11):
    from typing import Never, NoReturn
else:
    Never, NoReturn = any, any

from django.db import models

__all__ = [
    "DBViewQuerySet",
]


class DBViewQuerySet(models.QuerySet):
    @classmethod
    def raise__method_not_allowed(cls, *args, **kwargs) -> NoReturn:
        raise AssertionError(
            f"Method is not allowed, for class '{cls.__name__}' due to it's db view"
        )

    def _batched_insert(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def bulk_create(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def bulk_update(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def create(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def delete(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def get_or_create(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def update(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()

    def update_or_create(self, *args, **kwargs) -> Never:
        self.raise__method_not_allowed()
