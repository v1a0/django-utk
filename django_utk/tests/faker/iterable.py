from typing import Callable, Generator, Iterable, List, Tuple

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

from django_utk.utils.typehint import typehint


class RandGenerator(DataFactory):
    def getter(self, length: int, item_factory: callable) -> Generator:
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

    @typehint(DataFactory)
    def __call__(self) -> Generator:
        pass


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

    @typehint(RandGenerator)
    def __call__(self) -> Iterable:
        pass


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

    @typehint(RandIterable)
    def __call__(self) -> List:
        pass


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

    @typehint(RandIterable)
    def __call__(self, *, length: int) -> Tuple:
        pass
