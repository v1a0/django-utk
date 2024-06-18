import random
from typing import Callable

from django_utk.utils.lazy import LazyCallable


class RandInt(LazyCallable):
    wrapped = random.randint
    MIN = -2147483648  # PostgreSQL (4 bytes integer)
    MAX = +2147483647  # PostgreSQL (4 bytes integer)

    __call__: Callable[[int, int], int]

    def __init__(self, start: int = MIN, end: int = MAX):
        super(RandInt, self).__init__(start, end)


class RandFloat(LazyCallable):
    wrapped = random.uniform
    MIN = -1.7976931348623158e308
    MAX = +1.7976931348623158e308

    __call__: Callable[[int, int], int]

    def __init__(self, start: float = MIN, end: float = MAX):
        super(RandFloat, self).__init__(start, end)
