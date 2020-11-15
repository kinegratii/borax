# coding=utf8

class AttributeDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


AD = AttributeDict
