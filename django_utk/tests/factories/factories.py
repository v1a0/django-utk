from abc import ABC, ABCMeta, abstractmethod
from typing import Callable, Dict, List, Type

from django.db import models

from django_utk.tests.faker.base import DataFactory
from django_utk.utils.lazy import Lazy
from django_utk.utils.popattr import popattr
from django_utk.utils.typehint import typehint


class FieldFactory:
    @classmethod
    def from_any(cls, value: any) -> "FieldFactory":
        if callable(value):
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

    @classmethod
    def from_factory(cls, factory) -> "FactoryOptions":
        return cls(getattr(factory, "Meta", None), factory)

    def __init__(self, options, factory: "Factory"):
        self.model = getattr(options, "model", NotImplemented)
        self.fields = getattr(options, "fields", None)
        self.fields_set = getattr(options, "fields_set", dict())
        self.factory = factory


class FactoryMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        new_class: BaseFactory = super().__new__(cls, name, bases, attrs)  # noqa

        if not popattr(new_class, "__no_meta__", False):
            new_class._meta = FactoryOptions.from_factory(new_class)

            for base in reversed(bases):
                if issubclass(base, BaseFactory) and hasattr(base, "_meta"):
                    new_class._meta.fields_set.update(base._meta.fields_set)

            for attr_name, attr_value in attrs.items():

                is_field = FactoryMeta.is_field_attr(
                    attr_name,
                    attr_value,
                    attrs_list=new_class._meta.fields,
                )

                if is_field:
                    new_class._meta.fields_set[attr_name] = FieldFactory.from_any(
                        attr_value
                    )

            if new_class._meta.fields is None:
                new_class._meta.fields = list(new_class._meta.fields_set.keys())
            else:
                new_class._meta.fields_set = {
                    field_name: field_factory
                    for field_name, field_factory in new_class._meta.fields_set.items()
                    if field_name in new_class._meta.fields
                }

        return new_class

    @staticmethod
    def is_field_attr(attr_name: str, attr_value: any, attrs_list: list[str]):
        if attrs_list is not None:
            # attr is mentioned in Factory.Meta.fields
            return attr_name in attrs_list
        elif attr_name.startswith("__"):
            # attr is private
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


class SubFactory(Lazy):
    @typehint
    def ___new__(self, factory: Factory, **kwargs) -> "SubFactory":
        pass
