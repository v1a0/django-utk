from abc import ABC, abstractmethod
from functools import partial
from typing import Callable

from django.utils.deconstruct import deconstructible

from django_utk.validators.base import BaseValidator

__all__ = [
    "is_hash_valid",
    "is_valid_md5",
    "is_valid_sha1",
    "is_valid_sha256",
    "is_valid_sha512",
    "HashValidator",
    "MD5Validator",
    "SHA1Validator",
    "SHA256Validator",
    "SHA512Validator",
]


def is_hash_valid(value: str, *, length: int) -> bool:
    try:
        value = str(value)
        int(value, base=16)
    except (ValueError, TypeError):
        return False
    except Exception:
        return False
    else:
        return len(value) == length


is_valid_md5: Callable[[str], bool] = partial(is_hash_valid, length=32)
is_valid_sha1: Callable[[str], bool] = partial(is_hash_valid, length=40)
is_valid_sha256: Callable[[str], bool] = partial(is_hash_valid, length=64)
is_valid_sha512: Callable[[str], bool] = partial(is_hash_valid, length=128)


class HashValidator(BaseValidator, ABC):
    code = "invalid"

    @classmethod
    @property
    @abstractmethod
    def algo_name(cls) -> str:
        raise NotImplemented

    @classmethod
    @property
    def name(cls) -> str:
        return f"Invalid {cls.algo_name.upper()} sum"


@deconstructible
class MD5Validator(HashValidator):
    algo_name = "md5"
    validation = is_valid_md5


@deconstructible
class SHA1Validator(HashValidator):
    algo_name = "sha1"
    validation = is_valid_sha1


@deconstructible
class SHA256Validator(HashValidator):
    algo_name = "md5"
    validation = is_valid_sha256


@deconstructible
class SHA512Validator(HashValidator):
    algo_name = "sha512"
    validation = is_valid_sha512
