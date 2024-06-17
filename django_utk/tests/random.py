import random
import string
from typing import Iterable, Any

from django_utk.utils.lazy import LazyCallable


class RandInt(LazyCallable):
    caller = random.randint
    MIN = -2147483648  # PostgreSQL (4 bytes integer)
    MAX = +2147483647  # PostgreSQL (4 bytes integer)

    def __init__(self, start: int = MIN, end: int = MAX):
        super(RandInt, self).__init__(start, end)


class RandFloat(LazyCallable):
    caller = random.uniform
    MIN = -1.7976931348623158e308
    MAX = +1.7976931348623158e308

    def __init__(self, start: float = MIN, end: float = MAX):
        super(RandFloat, self).__init__(start, end)


class RandChoices(LazyCallable):
    caller = random.choices

    def __init__(self, choices: Iterable[Any]):
        super().__init__(choices)


class RandString(LazyCallable):
    alphabet = string.hexdigits
    LENGTH = 32

    def caller(self, length: int) -> str:
        return "".join(random.choices(self.alphabet, k=length))

    def __init__(self, length: int = LENGTH, *, alphabet: str = None):
        if alphabet is not None:
            self.alphabet = alphabet

        super().__init__(length=length)
