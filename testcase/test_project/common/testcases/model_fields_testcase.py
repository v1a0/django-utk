from abc import ABC, abstractmethod
from typing import Any, Mapping

from django.db import models
from django.db.models import Field

from django_utk.db.models.utils import get_model_meta as meta


class ModelFieldsTestCase(ABC):

    @property
    @abstractmethod
    def model(self) -> models.Model:
        raise NotImplemented

    @property
    @abstractmethod
    def required_fields(self) -> Mapping[str, Mapping[str, Any]]:
        raise NotImplemented

    def get_required_fields(self):
        return self.required_fields

    def test__fields(self):
        """
        Checking child-model's fields to make sure all parent's features in there. TODO: rewrite
        """
        required_fields = self.get_required_fields()

        model_meta = meta(self.model)
        model_fields = {field.attname: field for field in model_meta.fields}

        model_fields_names = set(model_fields.keys())
        required_fields_names = set(required_fields.keys())

        lost_fields_name = required_fields_names - model_fields_names

        self.assertFalse(
            lost_fields_name,
            f"Model does not implementing some of required fields: {lost_fields_name}",
        )

        for required_field_name, required_field_kw in required_fields.items():
            field: Field = model_fields[required_field_name]

            for kw_name, kw_value in required_field_kw.items():
                kw = getattr(field, kw_name)
                self.assertEqual(kw, kw_value)
