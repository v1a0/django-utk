import random

from django_utk.utils.lazy import LazyCallable

__all__ = [
    "RandInt",
    "RandFloat",
]


class RandInt(LazyCallable):
    wrapped = random.randint
    MIN = -2147483648  # PostgreSQL (4 bytes integer)
    MAX = +2147483647  # PostgreSQL (4 bytes integer)

    def __init__(self, a: int = MIN, b: int = MAX):
        super(RandInt, self).__init__(a=a, b=b)


class RandFloat(LazyCallable):
    wrapped = random.uniform
    MIN = -1e300
    MAX = +1e300

    def __init__(self, a: float = MIN, b: float = MAX):
        super(RandFloat, self).__init__(a=a, b=b)
