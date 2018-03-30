# coding=utf8
"""
A Lazy Creator for a Object.
"""

import operator

__all__ = ['LazyObject']


def proxy_method(func):
    def inner(self, *args):
        if self._wrapped is None:
            self._setup()
        return func(self._wrapped, *args)

    return inner


class LazyObject(object):
    _wrapped = None

    def __init__(self, func):
        self.__dict__['_setupfunc'] = func

    __getattr__ = proxy_method(getattr)

    def __setattr__(self, key, value):
        if key == '_wrapped':
            self.__dict__['_wrapped'] = value
        else:
            if self._wrapped is None:
                self._setup()
            setattr(self._wrapped, key, value)

    def _setup(self):
        self._wrapped = self._setupfunc()

    __getitem__ = proxy_method(operator.getitem)
    __bytes__ = proxy_method(bytes)
    __str__ = proxy_method(str)
    __bool__ = proxy_method(bool)
