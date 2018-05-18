# coding=utf8


from collections import namedtuple

__all__ = ['EMPTY', 'AliasItem', "AliasDictionary"]

EMPTY = object()

AliasItem = namedtuple('AliasItem', 'alias key value')


class AliasDictionary:
    """
    A dictionary in support of access value with alias name.
    """

    def __init__(self, data, aliases=None):
        self._aliases = aliases or {}
        self._data = data

    def add_aliases(self, **kwargs):
        self._aliases.update(**kwargs)

    def get(self, name, default=None):
        key = self._aliases.get(name, name)
        return self._data.get(key, default)

    def get_item(self, name, default=EMPTY, raise_exception=False):
        if default is EMPTY:
            raise_exception = True

        if name in self._data:
            key, value = name, self._data[name]
        else:
            if name in self._aliases:
                _f_key = self._aliases[name]
                if _f_key in self._data:
                    key, value = _f_key, self._data[_f_key]
                else:
                    if raise_exception:
                        raise KeyError('{}'.format(name))
                    else:
                        key, value = None, default
            else:
                if raise_exception:
                    raise KeyError('{}'.format(name))
                else:
                    key, value = None, default
        return AliasItem(name, key, value)

    def get_available_items(self):
        for key, value in self._data.items():
            aliases = [k for k, v in self._aliases.items() if v == key]
            yield key, value, aliases
