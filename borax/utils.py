# coding=utf8

from functools import reduce
import collections


def force_iterable(obj):
    if not isinstance(obj, collections.Iterable) or isinstance(obj, str):
        return [obj]
    return obj


def safe_chain_getattr(obj, attr):
    """recourse through an attribute chain to get the ultimate value."""
    return reduce(getattr, attr.split('.'), obj)


def chain_getattr(obj, attr, value=None):
    """Get chain attribute for an object.
    """
    try:
        func_or_value = safe_chain_getattr(obj, attr)
        return func_or_value() if hasattr(func_or_value, '__call__') else func_or_value
    except AttributeError:
        return value
