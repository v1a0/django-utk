from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.utils import run_10k_times


class RandNumericTestCase:
    NumericFactory = NotImplemented

    a = NotImplemented
    b = NotImplemented
    return_type = NotImplemented

    @run_10k_times
    def test__default(self):
        rand_fct = self.NumericFactory()
        value = rand_fct()

        self.assertIsInstance(value, self.return_type)
        self.assertGreaterEqual(value, self.NumericFactory.MIN)
        self.assertLessEqual(value, self.NumericFactory.MAX)

    @run_10k_times
    def test__gte(self):
        rand_fct_1 = self.NumericFactory()
        rand_fct_2 = self.NumericFactory(self.a)
        rand_fct_3 = self.NumericFactory(a=self.a)

        value_1 = rand_fct_1(a=self.a)
        value_2 = rand_fct_2()
        value_3 = rand_fct_3()

        self.assertGreaterEqual(value_1, self.a)
        self.assertGreaterEqual(value_2, self.a)
        self.assertGreaterEqual(value_3, self.a)

        self.assertLessEqual(value_1, self.NumericFactory.MAX)
        self.assertLessEqual(value_2, self.NumericFactory.MAX)
        self.assertLessEqual(value_3, self.NumericFactory.MAX)

    @run_10k_times
    def test__lte(self):
        rand_fct_1 = self.NumericFactory()
        rand_fct_2 = self.NumericFactory(b=self.a)

        value_1 = rand_fct_1(b=self.a)
        value_2 = rand_fct_2()

        self.assertGreaterEqual(value_1, self.NumericFactory.MIN)
        self.assertGreaterEqual(value_2, self.NumericFactory.MIN)

        self.assertLessEqual(value_1, self.a)
        self.assertLessEqual(value_2, self.a)

    @run_10k_times
    def test__gte_lte(self):
        rand_fct_1 = self.NumericFactory()
        rand_fct_2 = self.NumericFactory(self.a, self.b)
        rand_fct_3 = self.NumericFactory(a=self.a, b=self.b)
        rand_fct_4 = self.NumericFactory(a=self.a)
        rand_fct_5 = self.NumericFactory(b=self.b)

        value_1 = rand_fct_1(a=self.a, b=self.b)
        value_2 = rand_fct_2()
        value_3 = rand_fct_3()
        value_4 = rand_fct_4(b=self.b)
        value_5 = rand_fct_5(a=self.a)

        self.assertGreaterEqual(value_1, self.a)
        self.assertGreaterEqual(value_2, self.a)
        self.assertGreaterEqual(value_3, self.a)
        self.assertGreaterEqual(value_4, self.a)
        self.assertGreaterEqual(value_5, self.a)

        self.assertLessEqual(value_1, self.b)
        self.assertLessEqual(value_2, self.b)
        self.assertLessEqual(value_3, self.b)
        self.assertLessEqual(value_4, self.b)
        self.assertLessEqual(value_5, self.b)


class RandIntTestCase(RandNumericTestCase, TestCase):
    NumericFactory = faker.RandInt

    a = 42
    b = a + a
    return_type = int


class RandFloatTestCase(RandNumericTestCase, TestCase):
    NumericFactory = faker.RandFloat

    a = 42.42
    b = a + a
    return_type = float
