from functools import wraps


def typehint(typed_method: callable = None, *, source: type = None):
    """
    Method decorator for conveniently adding type hints to child class methods
    without initializing the method body with `super` call and be left `pass`

    >>> from django_utk.utils.typehint import typehint
    >>>
    >>> class Calculator:
    >>>     def is_greater(self, a, b):
    >>>         return a > b
    >>>
    >>>     def is_lower(self, a, b):
    >>>         return a < b
    >>>
    >>> class TypedCalculator(Calculator):
    >>>     @typehint               # simple way
    >>>     def is_greater(self, a: int, b: int) -> bool:
    >>>         pass
    >>>
    >>>     @typehint(Calculator)   # better performance
    >>>     def is_lower(self, a: int, b: int) -> bool:
    >>>         pass
    >>>
    >>>
    >>> calc = TypedCalculator()
    >>> print(calc.is_greater(1, 0))    # True
    >>> print(calc.is_lower(1, 0))      # False
    """

    if not typed_method and not source:
        raise ValueError(
            f"{typehint.__repr__()} decorator require at least one of two arguments: 'typed_method' or 'source'"
        )

    if isinstance(typed_method, type):
        """
        Handle source as first argument

        >>> class Child(Parent):
        >>>     @typehint(Parent)
        >>>     def method(...):
        >>>         pass
        """
        typed_method, source = None, typed_method

    def typehint_wrapper(method: callable):
        if source:
            super_method = getattr(source, method.__name__)
            # patch for class-methods
            super_method = getattr(super_method, "__func__", super_method)
            super_proxy = wraps(method)(super_method)

        else:

            @wraps(method)
            def super_proxy(self, *args, **kwargs):
                if isinstance(self, type):
                    cls = self

                    if method.__name__ == "__new__":
                        args = (cls, *args)
                else:
                    cls = type(self)

                super_obj = super(cls, self)
                super_method = getattr(super_obj, method.__name__)

                return super_method(*args, **kwargs)

        return super_proxy

    if typed_method:
        return typehint_wrapper(typed_method)
    else:
        return typehint_wrapper
