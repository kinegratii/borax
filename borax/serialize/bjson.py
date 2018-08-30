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
