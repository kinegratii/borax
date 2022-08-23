from collections import OrderedDict

from typing import Dict

__all__ = ['Item', 'ConstChoices']


class Item:
    _order = 0

    def __init__(self, value, display=None, *, order=None):
        self._value = value
        if display is None:
            self._display = str(value)
        else:
            self._display = str(display)
        if order is None:
            Item._order += 1
            self.order = Item._order
        else:
            self.order = order

    @property
    def value(self):
        return self._value

    @property
    def display(self):
        return self._display

    @property
    def label(self):
        return self._display

    def __str__(self):
        return f'<{self.__class__.__name__} value={self.value!r} label={self.label!r}>'

    __repr__ = __str__


class ChoicesMetaclass(type):
    def __new__(cls, name, bases, attrs):

        fields = {}  # {<name>:<BItem>}

        parents = [b for b in bases if isinstance(b, ChoicesMetaclass)]
        for kls in parents:
            for field_name in kls.fields:
                fields[field_name] = kls.fields[field_name]

        for k, v in attrs.items():
            if k.startswith('_'):
                continue
            if isinstance(v, Item):
                fields[k] = v
            elif isinstance(v, (tuple, list)) and len(v) == 2:
                fields[k] = Item(v[0], v[1])
            elif isinstance(v, (int, float, str, bytes)):
                fields[k] = Item(v)

        fields = OrderedDict(sorted(fields.items(), key=lambda x: x[1].order))
        for field_name, item in fields.items():
            attrs[field_name] = item.value  # override the exists attrs __dict__

        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls._fields = fields
        return new_cls

    @property
    def fields(cls) -> Dict[str, Item]:
        return dict(cls._fields)

    @property
    def choices(cls) -> list:
        return [(item.value, item.label) for _, item in cls.fields.items()]

    @property
    def names(cls) -> tuple:
        return tuple(cls.fields.keys())

    @property
    def values(cls) -> tuple:
        return tuple([value for value, _ in cls.choices])

    @property
    def displays(cls) -> tuple:
        return tuple([display for _, display in cls.choices])

    @property
    def labels(cls) -> tuple:
        return cls.displays

    @property
    def display_lookup(cls) -> dict:
        return {value: label for value, label in cls.choices}

    def __contains__(self, item):
        return item in self.values

    def __iter__(self):
        for item in self.choices:
            yield item

    def __len__(self):
        return len(self.choices)

    # API
    def is_valid(cls, value) -> bool:
        return value in cls.display_lookup

    def get_value_display(cls, value, default=None):
        return cls.display_lookup.get(value, default)


class ConstChoices(metaclass=ChoicesMetaclass):
    pass
