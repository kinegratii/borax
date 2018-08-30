# coding=utf8

import json

__all__ = ['EncoderMixin', 'BJSONEncoder']


class EncoderMixin:
    def __json__(self):
        pass


class BJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__json__'):
            return o.__json__()
        return super().default(o)


def dumps(obj, **kwargs):
    return json.dumps(obj, cls=BJSONEncoder, **kwargs)


def dump(obj, fp, **kwargs):
    return json.dump(obj, fp, cls=BJSONEncoder, **kwargs)
