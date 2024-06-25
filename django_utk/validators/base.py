from abc import ABC, abstractmethod

from django.core.exceptions import ValidationError


class BaseValidator(ABC):
    message = "Invalid value"
    code = "invalid"

    @staticmethod
    @abstractmethod
    def validation(value: any) -> callable:
        raise NotImplemented

    def __call__(self, value: str):
        if not self.validation(value):
            raise ValidationError(message=self.message, code=self.code)
