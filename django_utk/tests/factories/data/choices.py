import random
from typing import Iterable, Any, Callable

from django_utk.utils.lazy import LazyCallable


class RandChoices(LazyCallable):
    wrapped = random.choices

    __call__: Callable[[], Any]

    def __init__(self, choices: Iterable[Any]):
        super().__init__(choices)
