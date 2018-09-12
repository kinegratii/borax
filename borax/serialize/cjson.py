# coding=utf8
import json
from functools import singledispatch

__all__ = ['to_serializable', 'dumps', 'dump']


@singledispatch
def to_serializable(obj):
    raise TypeError('Type {} is not JSON serializable'.format(obj.__class__.__name__))


def dumps(obj, **kwargs):
    return json.dumps(obj, default=to_serializable, **kwargs)


def dump(obj, fp, **kwargs):
    return json.dump(obj, fp, default=to_serializable, **kwargs)
