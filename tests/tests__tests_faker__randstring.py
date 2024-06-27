import string
from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.utils import run_100_times

rand_int = faker.RandInt(1, 42)


class RandStringTestCase(TestCase):
    @run_100_times
    def assertResultValid(
        self,
        string_factory: callable,
        length: int = faker.RandString.LENGTH,
        alphabet: set = faker.RandString.ALPHABET,
    ):
        result = string_factory()

        self.assertEqual(len(result), length)
        self.assertEqual(len(set(result) - set(alphabet)), 0)

    def test_default(self):
        string_fct = faker.RandString()

        self.assertResultValid(string_fct)

    @run_100_times
    def test__alphabet(self):
        string_len = rand_int()
        alphabet = string.printable[: min(len(string.printable), rand_int())]
        string_fct = faker.RandString(string_len, alphabet=alphabet)
        self.assertResultValid(string_fct, string_len, set(alphabet))


class RandFilenameTestCase(TestCase):
    @run_100_times
    def assertResultValid(
        self,
        filename_factory: callable,
        extensions: list[str] = faker.RandFilename.EXTENSIONS,
        length: int = faker.RandFilename.LENGTH,
        alphabet: set = faker.RandFilename.ALPHABET,
    ):
        result: str = filename_factory()
        name, ext = result.split(".", 1)

        self.assertEqual(len(name), length)
        self.assertEqual(len(set(name) - set(alphabet)), 0)
        self.assertIn(ext, extensions)

    def test_default(self):
        string_fct = faker.RandFilename()
        self.assertResultValid(string_fct)

    @run_100_times
    def test__alphabet(self):
        string_len = rand_int()
        alphabet = string.printable[: min(len(string.printable), rand_int())]
        filename_fct = faker.RandFilename(string_len, alphabet=alphabet)
        self.assertResultValid(filename_fct, length=string_len, alphabet=set(alphabet))

    @run_100_times
    def test__extensions(self):
        rand_str = faker.RandString()
        extensions = [rand_str() for _ in range(rand_int())]
        filename_fct = faker.RandFilename(extensions=extensions)
        self.assertResultValid(filename_fct, extensions=extensions)
