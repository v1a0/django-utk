import uuid
from abc import ABC, abstractmethod
from functools import partial
from typing import Callable

from django.utils.deconstruct import deconstructible

from django_utk.validators.base import BaseValidator


def is_valid_uuid(value: str = None, *args, version: int = 4) -> bool:
    """
    Validate value as UUID4
    """
    try:
        uuid.UUID(str(value), *args, version=version)
    except (ValueError, TypeError):
        return False
    except Exception:
        return False
    else:
        return True


is_valid_uuid1: Callable[[str], bool] = partial(is_valid_uuid, version=1)
is_valid_uuid2: Callable[[str], bool] = partial(is_valid_uuid, version=2)
is_valid_uuid3: Callable[[str], bool] = partial(is_valid_uuid, version=3)
is_valid_uuid4: Callable[[str], bool] = partial(is_valid_uuid, version=4)
is_valid_uuid5: Callable[[str], bool] = partial(is_valid_uuid, version=5)


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


@deconstructible
class UUID1Validator(UUIDValidator):
    uuid_version = 1
    validation = is_valid_uuid1


@deconstructible
class UUID2Validator(UUIDValidator):
    uuid_version = 2
    validation = is_valid_uuid2


@deconstructible
class UUID3Validator(UUIDValidator):
    uuid_version = 3
    validation = is_valid_uuid3


@deconstructible
class UUID4Validator(UUIDValidator):
    uuid_version = 4
    validation = is_valid_uuid4


@deconstructible
class UUID5Validator(UUIDValidator):
    uuid_version = 5
    validation = is_valid_uuid5
