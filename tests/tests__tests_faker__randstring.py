import random
import string
from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.run_n_times import run_100_times


class RandStringTestCase(TestCase):

    A = 42
    ALPHABET = string.printable

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

    def test__alphabet(self):
        for alphabet_len in range(1, self.A):
            alphabet = random.choices(self.ALPHABET, k=alphabet_len)

            for string_len in range(1, self.A):
                string_fct = faker.RandString(string_len, alphabet=alphabet)

                self.assertResultValid(string_fct, string_len, set(alphabet))
