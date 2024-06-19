from abc import ABCMeta, abstractmethod, ABC
from typing import Type, Callable, Dict

from django.db import models

from django_utk.utils.lazy import Lazy, LazyCallable
from tests.faker.sequences import BaseSequence


class SubFactory(Lazy):
    pass


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
    fields: Dict[str, "FieldFactory"]
    factory: "Factory"

    @classmethod
    def from_factory(cls, factory) -> "FactoryOptions":
        return cls(getattr(factory, "Meta", None), factory)

    def __init__(self, options, factory: "Factory"):
        self.model = getattr(options, "model", NotImplemented)
        self.fields = getattr(options, "fields", {})
        self.factory = factory


class FactoryMeta(ABCMeta):
    def __new__(cls, name, bases, attrs):
        new_class: BaseFactory = super().__new__(cls, name, bases, attrs)  # noqa

        if not getattr(new_class, "__no_meta__", False):
            new_class._meta = FactoryOptions.from_factory(new_class)

            for base in reversed(bases):
                if issubclass(base, BaseFactory) and hasattr(base, "_meta"):
                    new_class._meta.fields.update(base._meta.fields)

            for attr_name, attr_value in attrs.items():

                is_attr_method = FactoryMeta.is_attr_method(attr_name, attr_value)

                if not is_attr_method:
                    new_class._meta.fields[attr_name] = FieldFactory.from_any(
                        attr_value
                    )

        return new_class

    @staticmethod
    def is_attr_method(attr_name: str, attr_value: any):
        return callable(attr_value) and not isinstance(
            attr_value, (SubFactory, BaseSequence, Lazy, LazyCallable)
        )


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
                for field_name, field_getter in cls.get_fields_defaults()
            },
            **{
                kwarg_name: FieldFactory.from_any(kwarg_value)
                for kwarg_name, kwarg_value in kwargs
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
        return cls._meta.fields

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
