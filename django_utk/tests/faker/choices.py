import random
from typing import Any, Iterable

from django_utk.tests.faker.base import DataFactory

__all__ = [
    "RandChoices",
    "RandChoice",
]

from django_utk.utils.typehint import typehint


class RandChoices(DataFactory):
    getter = random.choices

    def __init__(
        self,
        population: Iterable[Any],
        k=1,
        *,
        weights: list[int] = None,
        cum_weights: list[int] = None,
    ):
        super().__init__(
            population=population,
            weights=weights,
            cum_weights=cum_weights,
            k=k,
        )

    @typehint(DataFactory)
    def __call__(
        self,
        *,
        population: Iterable[Any],
        k: int = 1,
        weights: list[int] = None,
        cum_weights: list[int] = None,
    ) -> list:
        pass


class RandChoice(RandChoices):
    def __init__(
        self,
        population: Iterable[Any],
        *,
        weights: list[int] = None,
        cum_weights: list[int] = None,
    ):
        super().__init__(
            population=population,
            weights=weights,
            cum_weights=cum_weights,
            k=1,
        )

    def getter(self, *args, **kwargs):
        try:
            return super().getter(*args, **kwargs)[0]
        except IndexError:
            return None

    @typehint(RandChoices)
    def __call__(
        self,
        *,
        population: Iterable[Any] = None,
        k: int = 1,
        weights: list[int] = None,
        cum_weights: list[int] = None,
    ):
        pass
