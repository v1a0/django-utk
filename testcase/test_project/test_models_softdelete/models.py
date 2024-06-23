from django.db.models.manager import BaseManager

from django_utk.db.models.softdelete import managers, models, querysets


class SomeQS(querysets.SoftDeleteQuerySet):
    def asdf(self):
        pass


SomeManager = BaseManager.from_queryset(SomeQS)


print(managers.SoftDeleteManager.__dict__)
