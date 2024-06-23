import random
from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.tests import faker


class RandChoicesTestCase(TestCase):

    A = 42
    B = 10_000

    def test__default(self):
        sequence_fct = faker.Sequence()

        for i in range(self.B):
            self.assertEqual(sequence_fct(), i)

    def test__start(self):
        sequence_fct = faker.Sequence(start=self.A)

        for i in range(self.A, self.B):
            self.assertEqual(sequence_fct(), i)

    def test__end(self):
        sequence_fct = faker.Sequence(end=self.A)

        for i in range(self.A):
            self.assertEqual(sequence_fct(), i)

        with self.assertRaises(StopIteration):
            sequence_fct()

    def test__start_end(self):
        sequence_fct = faker.Sequence(start=self.A, end=self.B)

        for i in range(self.A, self.B):
            self.assertEqual(sequence_fct(), i)

        with self.assertRaises(StopIteration):
            sequence_fct()

    def test__step(self):
        sequence_fct = faker.Sequence(step=self.A)

        for i in range(self.B):
            self.assertEqual(sequence_fct(), (i * self.A))

    def test__handler(self):
        handler = MagicMock()

        sequence_fct = faker.Sequence(handler)

        for i in range(self.B):
            self.assertEqual(handler.call_count, i)
            sequence_fct()
            self.assertEqual(handler.call_args[0][0], i)


class ForEachTestCase(TestCase):

    ITEMS_LEN = 100
    ITEMS = [i for i in range(ITEMS_LEN)]

    @classmethod
    def setUpClass(cls):
        random.shuffle(cls.ITEMS)

    def test__default(self):
        foreach_fct = faker.ForEach(self.ITEMS)

        for i in range(self.ITEMS_LEN):
            self.assertEqual(foreach_fct(), self.ITEMS[i])
