import json
from datetime import datetime, date
from functools import singledispatch

__all__ = ['encode_object', 'encoder', 'dumps', 'dump', 'CJSONEncoder']


def encode_object(obj):
    if hasattr(obj, '__json__'):
        return obj.__json__()
    raise TypeError(f'Type {obj.__class__.__name__} is not JSON serializable')


def _unregister(self, cls):
    self.register(cls, encode_object)


encoder = singledispatch(encode_object)
encoder.unregister = _unregister.__get__(encoder)  # see more detail on https://stackoverflow.com/a/28060251


def dumps(obj, **kwargs):
    return json.dumps(obj, default=encoder, **kwargs)


def dump(obj, fp, **kwargs):
    return json.dump(obj, fp, default=encoder, **kwargs)


encoder.register(datetime, lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S'))
encoder.register(date, lambda obj: obj.strftime('%Y-%m-%d'))


class CJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return encoder(o)
