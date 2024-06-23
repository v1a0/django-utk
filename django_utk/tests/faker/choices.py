import random
from typing import Any, Callable, Iterable

from django_utk.utils.lazy import LazyCallable

__all__ = [
    "RandChoices",
    "RandChoice",
]


class RandChoices(LazyCallable):
    wrapped = random.choices

    def __init__(
        self,
        population: Iterable[Any],
        k=1,
        *,
        weights: list[int] = None,
        cum_weights: list[int] = None,
    ):
        super().__init__(
            population=population, weights=weights, cum_weights=cum_weights, k=k
        )


class RandChoice(RandChoices):
    def __init__(
        self,
        population: Iterable[Any],
        *,
        weights: list[int] = None,
        cum_weights: list[int] = None,
    ):
        super().__init__(
            population=population, weights=weights, cum_weights=cum_weights, k=1
        )

    def wrapped(self, **kwargs):
        try:
            return super().wrapped(**kwargs)[0]
        except IndexError:
            return None
