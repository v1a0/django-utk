import hashlib
import random
from unittest import TestCase
from unittest.mock import MagicMock

from django.core.exceptions import ValidationError

from django_utk.tests import faker
from django_utk.tests.utils import run_1k_times
from django_utk.validators.hashes import (
    HashValidator,
    MD5Validator,
    SHA1Validator,
    SHA256Validator,
    SHA512Validator,
    is_hash_valid,
    is_valid_md5,
    is_valid_sha1,
    is_valid_sha256,
    is_valid_sha512,
)

rand_int = faker.RandInt(1, 100)
big_int = faker.RandInt(1, int(faker.RandFloat.MAX))
not_hash = faker.RandString(length=rand_int(), alphabet="qwrtyuiopsghjklzxvnm")


class HashValidationTestCase(TestCase):

    @run_1k_times
    def assertValid(self, algo: callable, validation: callable):
        hash_sum = algo(random.randbytes(10)).hexdigest()
        self.assertTrue(validation(hash_sum))

    @run_1k_times
    def assertInvalid(self, validation: callable):
        self.assertFalse(validation(not_hash()))

    def test__is_valid_md5(self):
        self.assertValid(algo=hashlib.md5, validation=is_valid_md5)
        self.assertInvalid(validation=is_valid_md5)

    def test__is_valid_sha1(self):
        self.assertValid(algo=hashlib.sha1, validation=is_valid_sha1)
        self.assertInvalid(validation=is_valid_sha1)

    def test__is_valid_sha256(self):
        self.assertValid(algo=hashlib.sha256, validation=is_valid_sha256)
        self.assertInvalid(validation=is_valid_sha256)

    def test__is_valid_sha512(self):
        self.assertValid(algo=hashlib.sha512, validation=is_valid_sha512)
        self.assertInvalid(validation=is_valid_sha512)

    def test__is_hash_valid(self):
        hash_sum = str(hex(big_int()))
        self.assertTrue(is_hash_valid(value=hash_sum, length=len(hash_sum)))

    def test__is_hash_valid__exception(self):
        for ExceptionType in (
            ValueError,
            TypeError,
            MagicMock(spec=Exception),  # some unexpected exception
        ):
            hash_sum = MagicMock()
            hash_sum.__str__ = MagicMock()
            hash_sum.__len__ = MagicMock()
            hash_sum.__str__.side_effect = ExceptionType
            hash_sum.__len__.return_value = rand_int()
            self.assertFalse(is_hash_valid(value=hash_sum, length=len(hash_sum)))


class HashValidatorsTestCase(TestCase):
    @run_1k_times
    def assertValid(self, algo: callable, validator: HashValidator):
        hash_sum = algo(random.randbytes(10)).hexdigest()
        validator(hash_sum)

    @run_1k_times
    def assertInvalid(self, validator: HashValidator):
        with self.assertRaises(ValidationError):
            validator(not_hash())

    def test__MD5Validator(self):
        self.assertValid(algo=hashlib.md5, validator=MD5Validator())
        self.assertInvalid(validator=MD5Validator())

    def test__SHA1Validator(self):
        self.assertValid(algo=hashlib.sha1, validator=SHA1Validator())
        self.assertInvalid(validator=SHA1Validator())

    def test__SHA256Validator(self):
        self.assertValid(algo=hashlib.sha256, validator=SHA256Validator())
        self.assertInvalid(validator=SHA256Validator())

    def test__SHA512Validator(self):
        self.assertValid(algo=hashlib.sha512, validator=SHA512Validator())
        self.assertInvalid(validator=SHA512Validator())
