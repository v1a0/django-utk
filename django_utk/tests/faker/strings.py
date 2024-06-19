import random
import string

from django_utk.utils.lazy import LazyCallable


__all__ = [
    "RandString",
]


class RandString(LazyCallable):
    wrapped = None
    ALPHABET = string.hexdigits
    LENGTH = 32

    def __call__(self, length: int) -> str:
        return "".join(random.choices(self.alphabet, k=length))

    def __init__(self, length: int = LENGTH, *, alphabet: str = None):
        if alphabet is not None:
            self.alphabet = self.ALPHABET

        super().__init__(length=length)
