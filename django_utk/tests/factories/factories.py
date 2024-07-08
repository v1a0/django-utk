from abc import ABC, ABCMeta, abstractmethod
from types import GenericAlias
from typing import Callable, Dict, List, Type

from django.core.exceptions import FieldDoesNotExist
from django.db import models

from django_utk.utils.lazy import Lazy
from django_utk.utils.popattr import popattr
from django_utk.utils.typehint import typehint


class FieldFactory:
    @classmethod
    def from_any(cls, value: any) -> "FieldFactory":
        if callable(value) or isinstance(value, classmethod):
            return cls(value)
        else:
            return cls(Lazy(lambda: value))

    def __init__(self, getter: Callable):
        self.getter = getter

    def __call__(self):
        return self.getter()


class FactoryOptions:
    model: Type[models.Model]
    fields: List[str]
    fields_set: Dict[str, "FieldFactory"]
    factory: "Factory"
    validate_model_fields: bool

    @classmethod
    def from_factory(cls, factory) -> "FactoryOptions":
        return cls(getattr(factory, "Meta", None), factory)

    def __init__(self, options, factory: "Factory"):
        self.model = getattr(options, "model", NotImplemented)
        self.fields = getattr(options, "fields", None)
        self.fields_set = getattr(options, "fields_set", dict())
        self.factory = factory
        self.validate_model_fields = getattr(options, "validate_model_fields", True)


class FactoryMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        klass: BaseFactory = super().__new__(cls, name, bases, attrs)  # noqa

        if not popattr(klass, "__no_meta__", False):
            _meta = FactoryOptions.from_factory(klass)

            for base in reversed(bases):
                if issubclass(base, BaseFactory) and hasattr(base, "_meta"):
                    _meta.fields_set.update(base._meta.fields_set)

            for attr_name, attr_value in attrs.items():
                if _meta.fields:
                    is_field = attr_name in _meta.fields
                else:
                    is_field = FactoryMeta.is_attr_field(attr_name, attr_value)

                if not is_field:
                    continue

                if _meta.validate_model_fields:
                    assert attr_name in _meta.model._meta.fields, FieldDoesNotExist(
                        f"Model {_meta.model.__name__} doesn't have field named {attr_name!r}, "
                        f"only: {', '.join(_meta.model._meta.fields.keys())}"
                    )

                _meta.fields_set[attr_name] = FieldFactory.from_any(attr_value)

            if _meta.fields:
                _meta.fields_set = {
                    field_name: field_factory
                    for field_name, field_factory in _meta.fields_set.items()
                    if field_name in _meta.fields
                }
            else:
                _meta.fields = list(_meta.fields_set.keys())

            klass._meta = _meta

        return klass

    @staticmethod
    def is_attr_field(attr_name: str, attr_value: any):
        from django_utk.tests.faker.base import DataFactory

        if attr_name.startswith("__"):
            # attr is private
            return False
        elif isinstance(attr_value, (classmethod, property)):
            return False
        elif callable(attr_value):
            # attr is method or unknown callable property
            return isinstance(attr_value, (Lazy, DataFactory))
        else:
            # attr is set straight
            return True


class BaseFactory(ABC):

    @classmethod
    @abstractmethod
    def get_model(cls) -> type:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def get_fields_defaults(cls) -> dict[str, Callable]:
        return NotImplemented

    @classmethod
    def get_init_values(cls, **kwargs):
        return {
            **{
                field_name: field_getter()
                for field_name, field_getter in cls.get_fields_defaults().items()
                if field_name not in kwargs
            },
            **{
                kwarg_name: FieldFactory.from_any(kwarg_value)()
                for kwarg_name, kwarg_value in kwargs.items()
            },
        }

    @classmethod
    def init_obj(cls, **kwargs):
        model = cls.get_model()
        init_values = cls.get_init_values(**kwargs)
        return model(**init_values)

    @classmethod
    def create(cls, **kwargs):
        """
        Create a single instance
        """
        return cls.init_obj(**kwargs)

    @classmethod
    def create_batch(cls, count, **kwargs) -> list:
        """
        Create many of instances
        """
        return [cls.init_obj(**kwargs) for _ in range(count)]

    def __new__(cls, **kwargs):
        return cls.create(**kwargs)

    @classmethod
    def sub_factory(cls, **kwargs):
        return SubFactory(cls, **kwargs)


class Factory(BaseFactory, metaclass=FactoryMeta):
    __no_meta__ = True
    _meta: FactoryOptions

    @classmethod
    def get_model(cls) -> type:
        return cls._meta.model

    @classmethod
    def get_fields_defaults(cls) -> dict:
        return cls._meta.fields_set

    @classmethod
    def create(cls, **kwargs):
        """
        Create a single instance
        """
        obj = super().create(**kwargs)
        obj.save()
        return obj

    @classmethod
    def create_batch(cls, count, **kwargs) -> list:
        """
        Create many of instances
        """
        objs = super().create_batch(count, **kwargs)
        return cls._meta.model.objects.bulk_create(objs)

    __class_getitem__ = classmethod(GenericAlias)


class SubFactory(Lazy):
    @typehint
    def ___new__(self, factory: Factory, **kwargs) -> "SubFactory":
        pass
