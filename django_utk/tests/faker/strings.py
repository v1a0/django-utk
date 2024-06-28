import pathlib
import random
import string
from typing import Callable

from django_utk.tests.faker.base import DataFactory
from django_utk.utils.typehint import typehint

__all__ = [
    "RandString",
    "RandFilename",
    "RandPath",
    "RandFilePath",
]


class RandString(DataFactory):
    ALPHABET = string.hexdigits
    LENGTH = 32

    @staticmethod
    def getter(length: int | Callable, prefix: str, suffix: str, alphabet: str):
        if callable(length):
            length = length()

        return "{prefix}{string}{suffix}".format(
            prefix=prefix,
            string="".join(random.choices(alphabet, k=length)),
            suffix=suffix,
        )

    def __init__(
        self,
        length: int | Callable = LENGTH,
        *,
        prefix: str = None,
        suffix: str = None,
        alphabet: str = None,
        **kwargs,
    ):
        super().__init__(
            length=length,
            prefix=prefix or "",
            suffix=suffix or "",
            alphabet=alphabet or self.ALPHABET,
        )

    @typehint(DataFactory)
    def __call__(
        self,
        *,
        length: int | Callable = None,
        prefix: str = None,
        suffix: str = None,
        alphabet: str = None,
    ) -> str:
        pass


class RandFilename(RandString):
    LENGTH = 64
    ALPHABET = string.ascii_letters
    EXTENSIONS = [
        *["3dm", "3ds"],
        *["aac", "accdb", "ai", "aiff", "apk", "app", "asp", "aspx", "avi"],
        *["bat", "bin", "bmp"],
        *["c", "cer", "class", "cmd", "com", "conf", "cpp", "crt", "csv"],
        *["dat", "db", "dbf", "dll", "doc", "docx", "dmg", "dmp", "dxf"],
        *["eps", "exe"],
        *["fla", "flac", "flv"],
        *["gif", "gz", "gzip"],
        *["h", "htm", "html", "hqx", "htaccess"],
        *["ics", "iff", "inc", "ini", "iso", "iso"],
        *["jar", "java", "jpg", "js", "json", "jsp"],
        *["key"],
        *["log"],
        *["mov", "mp2", "mp3", "mp4", "mpeg", "mpg", "msg", "msi", "mswmm"],
        *["obj", "odp", "ods", "odt", "otp", "ots", "ott"],
        *["pdf", "pkg", "png", "pptx", "ps", "psd", "pub"],
        *["rar", "rb", "reg", "rpm", "rss", "rtf"],
        *["sav", "sh", "sitx", "sql", "svg", "swf", "sys"],
        *["tar", "tif", "tiff", "tmp", "torrent", "ttf", "txt"],
        *["v", "vcf", "vob"],
        *["wav", "webm", "wps", "xlr", "xls", "xlsx", "xml"],
        *["z", "zip", "7z"],
    ]

    def getter(self, *args, **kwargs):
        return "{name}.{extension}".format(
            name=super().getter(*args, **kwargs),
            extension=random.choices(self.extensions)[0],
        )

    def __init__(
        self,
        length: int = LENGTH,
        *,
        extensions: list[str] = None,
        alphabet: str = None,
    ):
        self.extensions = extensions or self.EXTENSIONS

        super().__init__(length=length, alphabet=alphabet)

    @typehint(RandString)
    def __call__(
        self,
        *,
        length: int | Callable = None,
        alphabet: str = None,
    ) -> str:
        pass


class RandPath(RandString):
    ALPHABET = string.ascii_letters

    def getter(self, *args, **kwargs):
        if callable(self.depth):
            depth = self.depth()
        else:
            depth = self.depth

        directories = [
            super(RandPath, self).getter(*args, **kwargs) for _ in range(depth)
        ]
        path = pathlib.Path().joinpath(self.root, *directories)

        return f"{path}{self.end}"

    def __init__(self, root: str = None, depth: int | Callable = None, end: str = "/"):
        from django_utk.tests.faker import RandInt

        self.root = root or ""
        self.depth = depth or RandInt(0, 5)
        self.end = end

        super().__init__(length=RandInt(1, 10), alphabet=self.ALPHABET)

    @typehint(RandString)
    def __call__(self) -> str:
        pass


class RandFilePath(RandPath):

    def getter(self, *args, **kwargs):
        path = super().getter(*args, **kwargs)
        file = self.filename_factory()
        return f"{path}{file}"

    def __init__(
        self,
        root: str = None,
        depth: int | Callable = None,
    ):
        self.filename_factory = RandFilename()

        super().__init__(root=root, depth=depth)

    @typehint(RandPath)
    def __call__(self) -> str:
        pass
