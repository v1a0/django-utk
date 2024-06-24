from abc import ABC, abstractmethod
from functools import partial

from django.utils.deconstruct import deconstructible

from django_utk.validators.base import BaseValidator


def is_hash_valid(value: str, length: int):
    try:
        int(value, base=16)
    except (ValueError, TypeError):
        return False
    finally:
        return len(value) == length


is_valid_md5 = partial(is_hash_valid, length=32)
is_valid_sha1 = partial(is_hash_valid, length=40)
is_valid_sha256 = partial(is_hash_valid, length=64)
is_valid_sha512 = partial(is_hash_valid, length=128)


class HashValidator(BaseValidator, ABC):
    code = "invalid"

    @classmethod
    @abstractmethod
    @property
    def algo_name(cls) -> str:
        raise NotImplemented

    @classmethod
    @property
    def name(cls) -> str:
        return f"Invalid {cls.algo_name.upper()} sum"


class MD5Validator(HashValidator):
    algo_name = "md5"
    validation = is_valid_md5


@deconstructible
class SHA1Validator(BaseValidator):
    algo_name = "sha1"
    validation = is_valid_sha1


@deconstructible
class SHA256Validator(BaseValidator):
    algo_name = "md5"
    validation = is_valid_sha256


@deconstructible
class SHA512Validator(BaseValidator):
    algo_name = "sha512"
    validation = is_valid_sha512
