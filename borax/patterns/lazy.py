"""
A Lazy Creator for a Object.
"""

import operator

__all__ = ['LazyObject']

EMPTY = object()


def proxy_method(func):
    def inner(self, *args):
        if self._wrapped is EMPTY:
            self._setup()
        return func(self._wrapped, *args)

    return inner


class LazyObject:
    _wrapped = None

    def __init__(self, func, args=None, kwargs=None):
        self.__dict__['_setupfunc'] = func
        self.__dict__['_args'] = args or []
        self.__dict__['_kwargs'] = kwargs or {}
        self._wrapped = EMPTY

    def _setup(self):
        self._wrapped = self._setupfunc(*self._args, **self._kwargs)

    __getattr__ = proxy_method(getattr)

    def __setattr__(self, key, value):
        if key == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is EMPTY:
                self._setup()
            setattr(self._wrapped, key, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is EMPTY:
            self._setup()
        delattr(self._wrapped, name)

    __getitem__ = proxy_method(operator.getitem)
    __class__ = property(proxy_method(operator.attrgetter("__class__")))
    __eq__ = proxy_method(operator.eq)
    __ne__ = proxy_method(operator.ne)
    __hash__ = proxy_method(hash)
    __bytes__ = proxy_method(bytes)
    __str__ = proxy_method(str)
    __bool__ = proxy_method(bool)
