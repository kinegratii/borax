# coding=utf8


import json
from datetime import datetime, date
from functools import singledispatch

__all__ = ['encode_object', 'encoder', 'dumps', 'dump', 'to_serializable']


def encode_object(obj):
    if hasattr(obj, '__json__'):
        return obj.__json__()
    raise TypeError('Type {} is not JSON serializable'.format(obj.__class__.__name__))


def _unregister(self, cls):
    self.register(cls, encode_object)


encoder = singledispatch(encode_object)
encoder.unregister = _unregister.__get__(encoder)  # see more detail on https://stackoverflow.com/a/28060251


def dumps(obj, **kwargs):
    return json.dumps(obj, default=encoder, **kwargs)


def dump(obj, fp, **kwargs):
    return json.dump(obj, fp, default=encoder, **kwargs)


to_serializable = encoder

encoder.register(datetime, lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S'))
encoder.register(date, lambda obj: obj.strftime('%Y-%m-%d'))
