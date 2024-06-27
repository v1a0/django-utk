import uuid

from django_utk.tests.faker import RandString

__all__ = [
    "UUID4",
]


class UUID4(RandString):
    @staticmethod
    def getter(*args, **kwargs):
        return str(uuid.uuid4().hex)

    def __init__(self):
        super().__init__()
