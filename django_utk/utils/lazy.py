from abc import ABC
from functools import partial


class Lazy(partial):
    """
    Lazy callable object with partial preset args and kwargs.

    Example:
        >>> import datetime
        >>> lazy_now = Lazy(datetime.datetime.now, tz=...)
        >>> lazy_now() # datetime.datetime(2077, 1, 1, 1, 1, 1, 000000)
        >>> lazy_now() # datetime.datetime(2077, 1, 1, 1, 1, 2, 000000)
        >>> lazy_now() # datetime.datetime(2077, 1, 1, 1, 1, 3, 000000)
    """
