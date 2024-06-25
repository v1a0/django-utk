from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.utils import run_1k_times

CHOICES = [42, 42.42, 42j, "foo", True, None, type, Exception, (), [], {}, ...]


class RandChoicesTestCase(TestCase):
    @run_1k_times
    def assertResultInChoices(self, choices_factory: faker.RandChoices, choices: list):
        for result in choices_factory():
            self.assertIn(result, choices)

    def test__default(self):
        for k in range(1, len(CHOICES) + len(CHOICES)):
            choices_fct = faker.RandChoices(CHOICES, k)
            self.assertResultInChoices(choices_fct, CHOICES)

    def test__no_choices(self):
        with self.assertRaises(IndexError) as _:
            choices_fct = faker.RandChoices([])
            choices_fct()


class RandChoiceTestCase(TestCase):
    def test__returns_one(self):
        choices_fct = faker.RandChoice(CHOICES)
        self.assertIn(choices_fct(), CHOICES)
