from typing import Callable

from django_utk.tests.faker import RandInt
from django_utk.tests.faker.base import DataFactory

__all__ = [
    "RandRange",
]


class RandRange(DataFactory):
    DEFAULT_MAX_SIZE = 100

    def getter(self, start: int, end: int | Callable, step: int) -> range:
        if callable(end):
            end = end()
        return range(start, end, step)

    def __init__(self, start: int = 0, end: int | Callable = None, step: int = 1):
        super(RandRange, self).__init__(
            start=start,
            end=end or RandInt(start + 1, start + self.DEFAULT_MAX_SIZE),
            step=step,
        )
