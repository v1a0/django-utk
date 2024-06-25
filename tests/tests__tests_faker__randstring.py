import string
from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.run_n_times import run_100_times

rand_int = faker.RandInt(1, 42)


class RandStringTestCase(TestCase):
    @run_100_times
    def assertResultValid(self, string_factory: callable, length: int, alphabet: set):
        result = string_factory()

        self.assertEqual(len(result), length)
        self.assertEqual(len(set(result) - set(alphabet)), 0)

    def test_default(self):
        string_fct = faker.RandString()

        self.assertResultValid(
            string_fct, faker.RandString.LENGTH, faker.RandString.ALPHABET
        )

    @run_100_times
    def test__alphabet(self):
        string_len = rand_int()
        alphabet = string.printable[: min(len(string.printable), rand_int())]
        string_fct = faker.RandString(string_len, alphabet=alphabet)
        self.assertResultValid(string_fct, string_len, set(alphabet))
