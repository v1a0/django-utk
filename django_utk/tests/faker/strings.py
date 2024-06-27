import random
import string

from django_utk.utils.lazy import LazyCallable

__all__ = [
    "RandString",
    "RandFilename",
]

from django_utk.utils.typehint import typehint


class RandString(LazyCallable):
    ALPHABET = string.hexdigits
    LENGTH = 32

    def wrapped(self):
        return "{prefix}{string}{suffix}".format(
            prefix=self.prefix,
            string="".join(random.choices(self.alphabet, k=self.length)),
            suffix=self.suffix,
        )

    def __init__(
        self,
        length: int = LENGTH,
        *,
        prefix: str = None,
        suffix: str = None,
        alphabet: str = None,
    ):
        self.length = length
        self.prefix = prefix or ""
        self.suffix = suffix or ""
        self.alphabet = alphabet or self.ALPHABET

        super().__init__()

    @typehint(LazyCallable)
    def __call__(self, *args, **kwargs) -> str:
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

    def wrapped(self):
        return "{name}.{extension}".format(
            name=super().wrapped(), extension=self.get_extension()
        )

    def get_extension(self):
        return random.choices(self.extensions)[0]

    def __init__(
        self,
        length: int = LENGTH,
        *,
        extensions: list[str] = None,
        alphabet: str = None,
    ):
        super().__init__(length=length, alphabet=alphabet)

        self.extensions = extensions or self.EXTENSIONS
