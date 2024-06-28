from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.tests import faker
from django_utk.validators.uuid import is_valid_uuid

rand_int = faker.RandInt(1, 10)


class RandGeneratorTestCase(TestCase):
    def test__default(self):
        length = rand_int()
        generator_fct = faker.RandGenerator(length)
        generator = generator_fct()

        self.assertEqual(len([i for i in generator]), length)

        with self.assertRaises(StopIteration):
            next(generator)

    def test__item_factory__callable(self):
        length = rand_int()
        items = []

        def item_factory():
            item = MagicMock()
            items.append(item)
            return item

        generator_fct = faker.RandGenerator(length, item_factory=item_factory)
        generator = generator_fct()
        generated_list = [item for item in generator]

        self.assertListEqual(items, generated_list)

        with self.assertRaises(StopIteration):
            next(generator)

    def test__item_factory__factory(self):
        length = rand_int()
        item_factory = faker.UUID4()

        generator_fct = faker.RandGenerator(length, item_factory=item_factory)

        for item in generator_fct():
            self.assertTrue(is_valid_uuid(item))


class RandListTestCase(TestCase):
    def test__default(self):
        length = rand_int()
        list_fct = faker.RandList(length)
        the_list = list_fct()

        self.assertIsInstance(the_list, list)
        self.assertEqual(len(the_list), length)


class RandTupleTestCase(TestCase):
    def test__default(self):
        length = rand_int()
        tuple_fct = faker.RandTuple(length)
        the_tuple = tuple_fct()

        self.assertIsInstance(the_tuple, tuple)
        self.assertEqual(len(the_tuple), length)
