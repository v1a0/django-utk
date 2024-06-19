from functools import wraps

from django_utk.tests import faker

from unittest import TestCase


TESTS_LOOP = range(1_000)


def many_runs(method: callable):
    @wraps(method)
    def many_running_method(*args, **kwargs):
        for _ in TESTS_LOOP:
            method(*args, **kwargs)

    return many_running_method


class RandIntTestCase(TestCase):
    TESTS_LOOP = range(1_000)

    @classmethod
    def setUpClass(cls):
        cls.rand_int = faker.RandInt()
        return super().setUpClass()

    @many_runs
    def test_default(self):
        value = self.rand_int()
        self.assertIsInstance(value, int)
        self.assertGreater(value, faker.RandInt.MIN)
        self.assertLess(value, faker.RandInt.MAX)

    # @many_runs
    # def test_gte(self):
    #     value = self.rand_int()
    #     self.assertIsInstance(value, int)
    #     self.assertGreater(value, faker.RandInt.MIN)
    #     self.assertLess(value, faker.RandInt.MAX)
    #
    # @many_runs
    # def test_lte(self):
    #     value = self.rand_int()
    #     self.assertIsInstance(value, int)
    #     self.assertGreater(value, faker.RandInt.MIN)
    #     self.assertLess(value, faker.RandInt.MAX)
