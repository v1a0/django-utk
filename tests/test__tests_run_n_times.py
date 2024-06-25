import string
from unittest import TestCase
from unittest.mock import MagicMock

from django_utk.tests import faker
from django_utk.tests.utils.run_n_times import (
    run_1k_times,
    run_10_times,
    run_10k_times,
    run_100_times,
    run_n_times,
)

small_int = faker.RandInt(2, 42)


class RunNTimesTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loopers = [
            (10, run_10_times),
            (100, run_100_times),
            (1_000, run_1k_times),
            (10_000, run_10k_times),
            # (100_000, run_100k_times),    # FIXME: sorry this thing is too slow
            # (1_000_000, run_1m_times),
        ] + [(n, run_n_times(n)) for n in range(small_int())]

        cls.rand_int = faker.RandInt()
        cls.rand_str = faker.RandString(alphabet=string.ascii_letters)
        cls.rand_float = faker.RandString(alphabet=string.ascii_letters)

    def test__all(self):
        def get_rand_args():
            return [self.rand_int() for _ in range(small_int())]

        def get_rand_kwargs():
            return {self.rand_str(): self.rand_float() for _ in range(small_int())}

        for n, looper in self.loopers:
            args = get_rand_args()
            kwargs = get_rand_kwargs()

            original_func = MagicMock()
            looped_func = looper(original_func)

            looped_func(*args, **kwargs)

            self.assertEqual(original_func.call_count, n)

            for i in range(n):
                self.assertListEqual(list(original_func.call_args_list[i].args), args)
                self.assertEqual(original_func.call_args_list[i].kwargs, kwargs)
