import uuid
from unittest import TestCase

from django_utk.tests import faker
from django_utk.tests.utils import run_1k_times
from django_utk.validators.uuid import is_valid_uuid1, is_valid_uuid4

uuid_length = 36
rand_int = faker.RandInt(1, (uuid_length - 1))
not_uuid = faker.RandString(length=rand_int())


class UUIDValidationTestCase(TestCase):

    @run_1k_times
    def assertValid(self, algo: callable, validation: callable):
        self.assertTrue(validation(value := algo()), f"{value=}")

    @run_1k_times
    def assertInvalid(self, validation: callable):
        self.assertFalse(validation(not_uuid()))

    def test__is_valid_uuid1(self):
        self.assertValid(algo=uuid.uuid1, validation=is_valid_uuid1)
        self.assertInvalid(validation=is_valid_uuid1)

    def test__is_valid_uuid4(self):
        self.assertValid(algo=uuid.uuid4, validation=is_valid_uuid4)
        self.assertInvalid(validation=is_valid_uuid4)
