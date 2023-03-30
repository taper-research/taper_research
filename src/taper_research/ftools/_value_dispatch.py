"""
Singledispatch based on value instead of type. Works similar to `functools.singledispatch`.
Uses python dictionary as cache.
"""


class _ValueDispatcher:
    """

    """

    def __init__(self, default_func):
        self.registry = {}
        self.default_func = default_func

    def register(self, value):
        """Decorator to register a new value handler"""

        def decorator(func):
            self.registry[value] = func
            return func

        return decorator

    def __call__(self, value, *args, **kwargs):
        """Dispatch to the appropriate value handler"""
        if value in self.registry:
            return self.registry[value](*args, **kwargs)
        else:
            return self.default_func(value, *args, **kwargs)


def dispatch_on_first_arg(func):
    """Usage

    >>> @dispatch_on_first_arg
    ... def handler(key, a, b):
    ...     raise NotImplementedError('Not implemented.')

    >>> @handler.register(1)
    ... def handler1(a, b):
    ...     return f"This is handler 1, {a=}, {b=}"

    >>> @handler.register(2)
    ... def handler2(a, b):
    ...     return f"This is handler 2, {a=}, {b=}"

    >>> # Dispatch based on value
    >>> handler(1, a=1, b=2) # "This is handler 1, a=1, b=2"
    >>> # This is handler 1
    >>> handler(2, a=1, b=2) # "This is handler 2, a=1, b=2"
    >>> # This is handler 2
    >>> handler(3, a=1, b=2) # NotImplementedError
    """
    dispatcher_ = _ValueDispatcher(func)
    return dispatcher_


def test_dispatch_on_first_arg():
    @dispatch_on_first_arg
    def handler(key, a, b):
        raise NotImplementedError('Not implemented.')

    @handler.register(1)
    def handler1(a, b):
        return f"This is handler 1, {a=}, {b=}"

    @handler.register(2)
    def handler2(a, b):
        return f"This is handler 2, {a=}, {b=}"

    # Dispatch based on value
    assert (handler(1, a=1, b=2)) == "This is handler 1, a=1, b=2"  # Output:
    # This is handler 1
    assert (handler(2, a=1, b=2)) == "This is handler 2, a=1, b=2"  # Output:
    # This is handler 2
    try:
        print(handler(3, a=1, b=2))  # Output:
        assert False
    except NotImplementedError as e:
        assert e.args[0] == 'Not implemented.'


if __name__ == '__main__':
    test_dispatch_on_first_arg()
