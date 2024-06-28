import io
import random
from typing import Callable

import django.core.files
import django.core.files.images

from django_utk.tests.faker.base import DataFactory, TypeCasting
from django_utk.tests.faker.numeric import RandInt
from django_utk.tests.faker.strings import RandFilename
from django_utk.utils.typehint import typehint

__all__ = [
    "RandBytes",
    "RandBytesIO",
    "RandFile",
    "RandImageFile",
]


class RandBytes(DataFactory):
    def getter(self, n: int | DataFactory | Callable):
        if callable(n):
            n = n()
        return random.randbytes(n)

    def __init__(self, n: int | DataFactory | Callable = None, **kwargs):
        if n is None:
            n = RandInt(0, (kilobyte := 1000))

        super().__init__(n=n, **kwargs)

    @typehint(DataFactory)
    def __call__(self, /, n: int | DataFactory | Callable = None) -> bytes:
        pass


class RandBytesIO(TypeCasting, RandBytes):
    cast = io.BytesIO

    @typehint(RandBytes)
    def __call__(self, /, n: int | DataFactory | Callable) -> io.BytesIO:
        pass


class RandFile(RandBytesIO):
    local_cast = django.core.files.File

    def getter(
        self, n: int | DataFactory | Callable, name: str | DataFactory | Callable
    ):
        if callable(name):
            name = name()
        return self.local_cast(super().getter(n), name=name)

    def __init__(
        self,
        n: int | DataFactory | Callable = None,
        name: str | DataFactory | Callable = None,
    ):
        if name is None:
            name = RandFilename()

        super().__init__(n=n, name=name)

    @typehint(RandBytesIO)
    def __call__(
        self,
        /,
        n: int | DataFactory | Callable,
        name: str | DataFactory | Callable,
    ) -> django.core.files.File:
        pass


class RandImageFile(RandFile):
    local_cast = django.core.files.images.ImageFile
    IMAGE_EXTENSIONS = [
        "jpg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "tif",
        "tiff",
        "webp",
        "svg",
        "ico",
        "heic",
    ]

    def __init__(
        self,
        n: int | DataFactory | Callable = None,
        name: str | DataFactory | Callable = None,
    ):
        if name is None:
            name = RandFilename(extensions=self.IMAGE_EXTENSIONS)

        super().__init__(n=n, name=name)

    @typehint(RandBytesIO)
    def __call__(
        self,
        *,
        n: int | DataFactory | Callable,
        name: str | DataFactory | Callable,
    ) -> django.core.files.images.ImageFile:
        pass
