import io
from unittest import TestCase

import django.core.files
import django.core.files.images

from django_utk.tests import faker
from django_utk.tests.utils import run_1k_times

big_int = faker.RandInt(1, 10000)
rand_str = faker.RandString()


class BaseBytesLikeTestCase:
    FactoryClass = NotImplemented
    expected_type = NotImplemented

    def get_size(self, item) -> int:
        raise NotImplemented

    @classmethod
    def setUpClass(cls):
        cls.byteslike_fct = cls.FactoryClass()
        super().setUpClass()

    @run_1k_times
    def test__default(self):
        self.assertIsInstance(self.byteslike_fct(), self.expected_type)

    @run_1k_times
    def test__n(self):
        n = big_int()

        bytes_fct_1 = self.FactoryClass(n=n)
        bytes_fct_2 = self.FactoryClass(n)
        bytes_fct_3 = self.FactoryClass()

        result_1 = bytes_fct_1()
        result_2 = bytes_fct_2()
        result_3 = bytes_fct_3(n=n)

        self.assertIsInstance(result_1, self.expected_type)
        self.assertIsInstance(result_2, self.expected_type)
        self.assertIsInstance(result_3, self.expected_type)

        self.assertEqual(self.get_size(result_1), n)
        self.assertEqual(self.get_size(result_2), n)
        self.assertEqual(self.get_size(result_3), n)


class RandBytesTestCase(BaseBytesLikeTestCase, TestCase):
    FactoryClass = faker.RandBytes
    expected_type = bytes

    def get_size(self, item: bytes) -> int:
        return len(item)


class RandBytesIOTestCase(BaseBytesLikeTestCase, TestCase):
    FactoryClass = faker.RandBytesIO
    expected_type = io.BytesIO

    def get_size(self, item: io.BytesIO):
        return item.getbuffer().nbytes


class RandFileTestCase(BaseBytesLikeTestCase, TestCase):
    FactoryClass = faker.RandFile
    expected_type = django.core.files.File

    def get_size(self, item: django.core.files.File):
        return item.size

    @run_1k_times
    def test__name(self):
        name = rand_str()

        bytes_fct_1 = self.FactoryClass(name=name)
        bytes_fct_3 = self.FactoryClass()

        result_1 = bytes_fct_1()
        result_3 = bytes_fct_3(name=name)

        self.assertEqual(result_1.name, name)
        self.assertEqual(result_3.name, name)


class RandImageFileTestCase(RandFileTestCase, TestCase):
    FactoryClass = faker.RandImageFile
    expected_type = django.core.files.images.ImageFile
