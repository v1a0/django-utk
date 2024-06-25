import random
import string

from django_utk.utils.lazy import LazyCallable

__all__ = [
    "RandString",
]

from django_utk.utils.typehint import typehint


class RandString(LazyCallable):
    ALPHABET = string.hexdigits
    LENGTH = 32

    def wrapped(self, length: int, alphabet: str):
        return "".join(random.choices(alphabet, k=length))

    def __init__(self, length: int = LENGTH, *, alphabet: str = None):
        if alphabet is None:
            alphabet = self.ALPHABET

        super().__init__(length=length, alphabet=alphabet)

    @typehint
    def __call__(self, *args, **kwargs) -> str:
        pass
