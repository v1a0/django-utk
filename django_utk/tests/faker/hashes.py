import hashlib
import string
from abc import ABC, abstractmethod

from django_utk.tests.faker.strings import RandString

__all__ = [
    "MD5HashSum",
    "SHA1HashSum",
    "SHA256HashSum",
    "SHA512HashSum",
]


class BaseHashSum(RandString, ABC):
    LENGTH = 1024

    @classmethod
    @property
    @abstractmethod
    def hash_algo(cls) -> callable:
        raise NotImplemented

    def wrapped(self):
        return self.hash_algo(super().wrapped().encode("utf-8")).hexdigest()

    def __init__(self):
        super().__init__()
        self.length = self.LENGTH


class MD5HashSum(BaseHashSum):
    hash_algo = hashlib.md5


class SHA1HashSum(BaseHashSum):
    hash_algo = hashlib.sha1


class SHA256HashSum(BaseHashSum):
    hash_algo = hashlib.sha256


class SHA512HashSum(BaseHashSum):
    hash_algo = hashlib.sha512
