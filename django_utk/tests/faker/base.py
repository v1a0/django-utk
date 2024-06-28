from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar

from django_utk.utils.typehint import typehint

T = TypeVar("T")
CastType = T | Callable[[Any], T]


class DataFactory(ABC):

    @abstractmethod
    def getter(self, *args, **kwargs):
        raise NotImplemented

    @classmethod
    def get(cls, *args, **kwargs):
        return cls(*args, **kwargs)()

    def __call__(self, **kwargs):
        kwargs = {**self.kwargs, **kwargs}
        return self.getter(*self.args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class DataFactoryMixin(ABC):
    pass


class TypeCasting(DataFactoryMixin):
    cast: CastType = lambda x: x

    def getter(self, *args, **kwargs):
        return self.cast(super().getter(*args, **kwargs))

    @typehint(DataFactory)
    def __call__(self, *args, **kwargs) -> CastType:
        pass
