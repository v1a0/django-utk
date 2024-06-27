from typing import Generator, Callable

from django_utk.tests.factories import Factory
from django_utk.tests.faker.base import DataFactory
from django_utk.tests.faker.numeric import RandInt
from django_utk.utils.lazy import Lazy

__all__ = [
    "RandGenerator",
    "RandIterable",
    "RandList",
    "RandTuple",
]


class RandGenerator(DataFactory):
    def getter(self, item_factory: callable, length: int) -> Generator:
        return (item_factory() for _ in range(length))

    def __init__(
        self,
        length: int,
        item_factory: Lazy | Factory | Callable = None,
    ):
        super(RandGenerator, self).__init__(
            length=length,
            item_factory=item_factory or RandInt(),
        )


class RandIterable(RandGenerator):
    def getter(self, *args, **kwargs) -> range:
        return self.cast(super().getter(*args, **kwargs))

    def __init__(
        self,
        length: int,
        item_factory: Lazy | Factory | Callable = None,
        cast: type = None,
    ):
        self.cast = cast or (lambda x: x)

        super(RandIterable, self).__init__(length=length, item_factory=item_factory)


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
