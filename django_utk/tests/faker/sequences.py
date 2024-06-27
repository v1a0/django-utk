from abc import ABC, abstractmethod
from typing import Any, Callable, Generator, Iterable, TypeVar

from django_utk.tests.faker.base import DataFactory
from django_utk.utils.typehint import typehint

__all__ = [
    "Sequence",
    "ForEach",
]


T = TypeVar("T")


class BaseSequence(DataFactory):
    def __init__(self, *args, **kwargs):
        self.sequencer: Generator[T, None, None] = self.get_sequencer()
        super().__init__()

    def __call__(self):
        return super().__call__()

    def getter(self):
        return next(self.sequencer)

    @abstractmethod
    def get_sequencer(self) -> Generator[Any, None, None]:
        raise NotImplemented


class Sequence(BaseSequence):
    @staticmethod
    def default_handler(x: int) -> int:
        return x

    def __init__(
        self,
        handler: Callable[[int], T] = None,
        start: int = 0,
        step: int = 1,
        end: int = None,
    ):
        self.handler = handler or self.default_handler
        self.start = start
        self.step = step
        self.end = end
        self.current = start

        super().__init__()

    def get_sequencer(self) -> Generator[Any, None, None]:
        if self.end is not None:
            for i in range(self.start, self.end, self.step):
                self.current = i
                yield self.handler(self.current)
        else:
            while True:
                yield self.handler(self.current)
                self.current += self.step

    @typehint(BaseSequence)
    def __call__(self) -> any:
        pass


class ForEach(BaseSequence):
    def __init__(self, items: Iterable[T]):
        self.items = items
        super(ForEach, self).__init__()

    def get_sequencer(self) -> Generator[Any, None, None]:
        for item in self.items:
            yield item

    @typehint(BaseSequence)
    def __call__(self) -> any:
        pass
