from django.db import models

__all__ = ["DeleteUsingManager"]


class DeleteUsingManager:
    """
    Replaces default Model.delete() feature (which users Collector.delete())
    by deleting using model's manager Model.objects.delete()

    Use "_objects_attr" class property to specify model's manager
    """

    _objects_attr = "objects"

    def delete(self, **kwargs):
        objects = getattr(type(self), self._objects_attr)
        return objects.filter(pk=self.pk).delete()
