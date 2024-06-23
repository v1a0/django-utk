from django.db import models
from django.utils.translation import gettext_lazy as _

from django_utk.db.models.softdelete import SoftDeleteQuerySet
from django_utk.db.models.softdelete.managers import SoftDeleteManager
from django_utk.db.models.utils import get_model_meta as meta

__all__ = [
    "BaseSoftDeleteModel",
    "SoftDeleteModel",
]


class BaseSoftDeleteModel:
    deleted_at = models.DateTimeField(
        verbose_name=_("Deleted at"),
        default=None,
        null=True,
        blank=True,
    )


class SoftDeleteModel(BaseSoftDeleteModel, models.Model):
    deleted_at: models.DateTimeField

    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def validate_existence(self, action: str):
        if self.pk is None:
            raise ValueError(
                "Failed to {action} object {obj_name} because it's {pk_attname} attribute is set to None".format(
                    action=action,
                    obj_name=meta(self).object_name,
                    pk_attname=meta(self).pk.attname,
                )
            )

    def delete(self, **kwargs):
        self.validate_existence(action=SoftDeleteModel.delete.__name__)
        model = type(self)
        model.all_objects.filter(pk=self.pk).delete()

    def restore(self):
        self.validate_existence(action=SoftDeleteModel.restore.__name__)
        model = type(self)
        model.all_objects.filter(pk=self.pk).restore()
