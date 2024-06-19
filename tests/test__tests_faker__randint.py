from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.utils import run_10k_times

A_NUMBER = 42
B_NUMBER = A_NUMBER + A_NUMBER


class RandIntTestCase(TestCase):
    @run_10k_times
    def test_default(self):
        rand_int = faker.RandInt()
        value = rand_int()

        self.assertIsInstance(value, int)
        self.assertGreaterEqual(value, faker.RandInt.MIN)
        self.assertLessEqual(value, faker.RandInt.MAX)

    @run_10k_times
    def test_gte(self):
        rand_int_1 = faker.RandInt()
        rand_int_2 = faker.RandInt(A_NUMBER)
        rand_int_3 = faker.RandInt(a=A_NUMBER)

        value_1 = rand_int_1(a=A_NUMBER)
        value_2 = rand_int_2()
        value_3 = rand_int_3()

        self.assertGreaterEqual(value_1, A_NUMBER)
        self.assertGreaterEqual(value_2, A_NUMBER)
        self.assertGreaterEqual(value_3, A_NUMBER)

        self.assertLessEqual(value_1, faker.RandInt.MAX)
        self.assertLessEqual(value_2, faker.RandInt.MAX)
        self.assertLessEqual(value_3, faker.RandInt.MAX)

    @run_10k_times
    def test_lte(self):
        rand_int_1 = faker.RandInt()
        rand_int_2 = faker.RandInt(b=A_NUMBER)

        value_1 = rand_int_1(b=A_NUMBER)
        value_2 = rand_int_2()

        self.assertGreaterEqual(value_1, faker.RandInt.MIN)
        self.assertGreaterEqual(value_2, faker.RandInt.MIN)

        self.assertLessEqual(value_1, A_NUMBER)
        self.assertLessEqual(value_2, A_NUMBER)

    @run_10k_times
    def test_gte_lte(self):
        rand_int_1 = faker.RandInt()
        rand_int_2 = faker.RandInt(A_NUMBER, B_NUMBER)
        rand_int_3 = faker.RandInt(a=A_NUMBER, b=B_NUMBER)
        rand_int_4 = faker.RandInt(a=A_NUMBER)
        rand_int_5 = faker.RandInt(b=B_NUMBER)

        value_1 = rand_int_1(a=A_NUMBER, b=B_NUMBER)
        value_2 = rand_int_2()
        value_3 = rand_int_3()
        value_4 = rand_int_4(b=B_NUMBER)
        value_5 = rand_int_5(a=A_NUMBER)

        self.assertGreaterEqual(value_1, A_NUMBER)
        self.assertGreaterEqual(value_2, A_NUMBER)
        self.assertGreaterEqual(value_3, A_NUMBER)
        self.assertGreaterEqual(value_4, A_NUMBER)
        self.assertGreaterEqual(value_5, A_NUMBER)

        self.assertLessEqual(value_1, B_NUMBER)
        self.assertLessEqual(value_2, B_NUMBER)
        self.assertLessEqual(value_3, B_NUMBER)
        self.assertLessEqual(value_4, B_NUMBER)
        self.assertLessEqual(value_5, B_NUMBER)
