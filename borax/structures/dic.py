# coding=utf8
"""See more detail at https://github.com/fabric/fabric/blob/1.13.1/fabric/utils.py.
"""


class AttributeDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            # to conform with __getattr__ spec
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *names):
        for name in names:
            value = self.get(name)
            if value:
                return value


class AliasDict(AttributeDict):
    def __init__(self, arg=None, aliases=None):
        init = super(AliasDict, self).__init__
        if arg is not None:
            init(arg)
        else:
            init()
        # Can't use super() here because of _AttributeDict's setattr override
        dict.__setattr__(self, 'aliases', aliases)

    def __setitem__(self, key, value):
        # Attr test required to not blow up when deepcopy'd
        if hasattr(self, 'aliases') and key in self.aliases:
            for aliased in self.aliases[key]:
                self[aliased] = value
        else:
            return super(AliasDict, self).__setitem__(key, value)

    def expand_aliases(self, keys):
        ret = []
        for key in keys:
            if key in self.aliases:
                ret.extend(self.expand_aliases(self.aliases[key]))
            else:
                ret.append(key)
        return ret
