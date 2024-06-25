import uuid
from abc import ABC, abstractmethod
from functools import partial

from django_utk.validators.base import BaseValidator


def is_valid_uuid(value: str = None, version: int = 4) -> bool:
    """
    Validate value as UUID4
    """
    try:
        uuid.UUID(value, version=version)
    except (ValueError, TypeError):
        return False
    finally:
        return True


is_valid_uuid1 = partial(is_valid_uuid, version=1)
is_valid_uuid2 = partial(is_valid_uuid, version=2)
is_valid_uuid3 = partial(is_valid_uuid, version=3)
is_valid_uuid4 = partial(is_valid_uuid, version=4)
is_valid_uuid5 = partial(is_valid_uuid, version=5)


class UUIDValidator(BaseValidator, ABC):
    code = "invalid"

    @classmethod
    @property
    @abstractmethod
    def uuid_version(cls) -> str:
        raise NotImplemented

    @classmethod
    @property
    def name(cls) -> str:
        return f"Invalid UUID{cls.uuid_version}"


class UUID1Validator(UUIDValidator):
    uuid_version = 1
    validation = is_valid_uuid1


class UUID2Validator(UUIDValidator):
    uuid_version = 2
    validation = is_valid_uuid2


class UUID3Validator(UUIDValidator):
    uuid_version = 3
    validation = is_valid_uuid3


class UUID4Validator(UUIDValidator):
    uuid_version = 4
    validation = is_valid_uuid4


class UUID5Validator(UUIDValidator):
    uuid_version = 5
    validation = is_valid_uuid5
