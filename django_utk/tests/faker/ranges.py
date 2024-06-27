from django_utk.tests.faker import RandInt
from django_utk.utils.lazy import LazyCallable

__all__ = [
    "RandRange",
]


class RandRange(LazyCallable):
    DEFAULT_MAX_SIZE = 100

    def wrapped(self) -> range:
        return range(
            self.start,
            self.end if not callable(self.end) else self.end(),
            self.step,
        )

    def __init__(self, start: int = 0, end: int | callable = None, step: int = 1):
        super(LazyCallable, self).__init__()

        self.start = start
        self.end = end or RandInt(start + 1, start + self.DEFAULT_MAX_SIZE)
        self.step = step
