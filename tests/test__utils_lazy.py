import string
from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.tests import faker
from django_utk.utils.lazy import Lazy

small_int = faker.RandInt(2, 42)
rand_str = faker.RandString(alphabet=string.ascii_letters)


class RunNTimesTestCase(TestCase):

    def test__no_args(self):
        args = []
        kwargs = {}
        original_func = MagicMock()
        lazy_func = Lazy(original_func)

        for i in range(small_int()):
            lazy_func()
            self.assertEqual(original_func.call_count, i + 1)
            self.assertListEqual(list(original_func.call_args_list[i].args), args)
            self.assertDictEqual(dict(original_func.call_args_list[i].kwargs), kwargs)

    def test__post_args(self):
        original_func = MagicMock()
        lazy_func = Lazy(original_func)

        for i in range(small_int()):
            lazy_func()
            self.assertEqual(original_func.call_count, i + 1)
            self.assertListEqual(list(original_func.call_args_list[i].args), [])
            self.assertDictEqual(dict(original_func.call_args_list[i].kwargs), {})

    def test__initial_args(self):
        initial_kwargs = {rand_str(): rand_str() for _ in range(small_int())}
        initial_args = [rand_str() for _ in range(small_int())]
        original_func = MagicMock()
        lazy_func = Lazy(original_func, *initial_args, **initial_kwargs)

        for i in range(small_int()):
            lazy_func()
            self.assertEqual(original_func.call_count, i + 1)
            self.assertListEqual(
                list(original_func.call_args_list[i].args), initial_args
            )
            self.assertDictEqual(
                dict(original_func.call_args_list[i].kwargs), initial_kwargs
            )

    def test__initial_args__and__post_args(self):
        args = [rand_str() for _ in range(small_int())]
        initial_args = [rand_str() for _ in range(small_int())]

        kwargs = {rand_str(): rand_str() for _ in range(small_int())}
        initial_kwargs = {rand_str(): rand_str() for _ in range(small_int())}

        calls_count = 0

        original_func = MagicMock()
        lazy_func = Lazy(original_func, *initial_args, **initial_kwargs)

        calls_count, _ = (calls_count + 1), lazy_func(*args, **kwargs)

        self.assertEqual(original_func.call_count, calls_count)
        self.assertListEqual(
            list(original_func.call_args_list[calls_count - 1].args),
            [*initial_args, *args],
        )
        self.assertDictEqual(
            dict(original_func.call_args_list[calls_count - 1].kwargs),
            {**kwargs, **initial_kwargs},
        )

        calls_count, _ = (calls_count + 1), lazy_func()

        self.assertEqual(original_func.call_count, calls_count)
        self.assertListEqual(
            list(original_func.call_args_list[calls_count - 1].args), initial_args
        )
        self.assertDictEqual(
            dict(original_func.call_args_list[calls_count - 1].kwargs), initial_kwargs
        )
