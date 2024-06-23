from abc import ABC, abstractmethod
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


class LazyCallable(ABC):
    def wrapped(self, *args, **kwargs):
        raise NotImplemented

    def __call__(self, **kwargs):
        return self.wrapped(**kwargs)

    def __init__(self, *args, **kwargs):
        self.wrapped = Lazy(self.wrapped, *args, **kwargs)
