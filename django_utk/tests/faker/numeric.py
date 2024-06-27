import random

from django_utk.tests.faker.base import DataFactory

__all__ = [
    "RandInt",
    "RandFloat",
]


class RandInt(DataFactory):
    getter = random.randint
    MIN = -2147483648  # PostgreSQL (4 bytes integer)
    MAX = +2147483647  # PostgreSQL (4 bytes integer)

    def __init__(self, a: int = MIN, b: int = MAX):
        super(RandInt, self).__init__(a=a, b=b)


class RandFloat(DataFactory):
    getter = random.uniform
    MIN = -1e300
    MAX = +1e300

    def __init__(self, a: float = MIN, b: float = MAX):
        super(RandFloat, self).__init__(a=a, b=b)
