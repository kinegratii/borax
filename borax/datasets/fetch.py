"""
fetch is a enhance module with fetch. And adjust the parameter order of calling to fit the habit.
"""
from functools import partial
from itertools import tee

__all__ = ['Empty', 'bget', 'fetch', 'ifetch', 'fetch_single', 'ifetch_multiple', 'ifetch_single', 'fetch_as_dict']


class Empty:
    pass


EMPTY = Empty()


def bget(obj, key, default=Empty):
    try:
        return obj[key]
    except (TypeError, KeyError):
        pass
    try:
        return getattr(obj, key)
    except (AttributeError, TypeError):
        pass

    if default is not EMPTY:
        return default

    raise ValueError(f'Item {obj!r} has no attr or key for {key!r}')


def ifetch_single(iterable, key, default=EMPTY, getter=None):
    """
    getter() g(item, key):pass
    """

    def _getter(item):
        if getter:
            custom_getter = partial(getter, key=key)
            return custom_getter(item)
        else:
            return partial(bget, key=key, default=default)(item)

    return map(_getter, iterable)


def fetch_single(iterable, key, default=EMPTY, getter=None):
    return list(ifetch_single(iterable, key, default=default, getter=getter))


def ifetch_multiple(iterable, *keys, defaults=None, getter=None):
    defaults = defaults or {}
    if len(keys) > 1:
        iters = tee(iterable, len(keys))
    else:
        iters = (iterable,)
    iters = [ifetch_single(it, key, default=defaults.get(key, EMPTY), getter=getter) for it, key in zip(iters, keys)]
    return iters


def ifetch(iterable, key, *keys, default=EMPTY, defaults=None, getter=None):
    if len(keys) > 0:
        keys = (key,) + keys
        return map(list, ifetch_multiple(iterable, *keys, defaults=defaults, getter=getter))
    else:
        return ifetch_single(iterable, key, default=default, getter=getter)


def fetch(iterable, key, *keys, default=EMPTY, defaults=None, getter=None):
    """Pick values from each field.

    >>> persons = [{'id': 1, 'name': 'Alice', 'age': 30},{'id': 2, 'name': 'John', 'age': 24}]
    >>> fetch(persons, 'name')
    ['Alice', 'John']

    >>> data = [[1, 2, 3, 4,], [11,12,13,14],[21,22,23,24]]
    >>> ones, threes = fetch(data, 0, 2)
    >>> ones
    [1, 11, 21]
    >>> threes
    [3, 13, 23]
    """
    return list(ifetch(iterable, key, *keys, default=default, defaults=defaults, getter=getter))


def fetch_as_dict(data, key_field, value_value):
    """Build a dict for a iterable data.

    >>> persons = [{'id': 1, 'name': 'Alice', 'age': 30},{'id': 2, 'name': 'John', 'age': 24}]
    >>> fetch_as_dict(persons, 'name', 'age')
    {'Alice': 30, 'John': 24}
    """
    return {bget(item, key_field): bget(item, value_value) for item in data}
