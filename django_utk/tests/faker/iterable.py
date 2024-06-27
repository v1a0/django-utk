from typing import Generator, Callable

from django_utk.tests.factories import Factory
from django_utk.tests.faker.numeric import RandInt
from django_utk.utils.lazy import Lazy, LazyCallable

__all__ = [
    "RandGenerator",
    "RandIterable",
    "RandList",
    "RandTuple",
]


class RandGenerator(LazyCallable):
    def wrapped(self) -> Generator:
        return (self.item_factory() for _ in range(self.length))

    def __init__(
        self,
        length: int,
        item_factory: Lazy | Factory | Callable = None,
    ):
        super(RandGenerator, self).__init__()

        self.length = length
        self.item_factory = item_factory or RandInt()


class RandIterable(RandGenerator):
    def wrapped(self) -> range:
        return self.cast(super().wrapped())

    def __init__(
        self,
        length: int,
        item_factory: Lazy | Factory | Callable = None,
        cast: type = None,
    ):
        super(RandIterable, self).__init__(length=length, item_factory=item_factory)

        self.cast = cast or (lambda x: x)


class RandList(RandIterable):
    def __init__(
        self,
        length: int,
        item_factory: Lazy | Factory | Callable = None,
    ):
        super(RandList, self).__init__(
            length=length,
            item_factory=item_factory,
            cast=list,
        )


class RandTuple(RandIterable):
    def __init__(
        self,
        length: int,
        item_factory: Lazy | Factory | Callable = None,
    ):
        super(RandTuple, self).__init__(
            length=length,
            item_factory=item_factory,
            cast=tuple,
        )
