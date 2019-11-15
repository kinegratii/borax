# coding=utf8

from collections import OrderedDict


class BItem:
    _order = 0

    def __init__(self, value, label=None, *, order=-1):
        self._value = value
        self._label = label
        if order is None:
            BItem._order += 1
            self.order = BItem._order
        else:
            self.order = order

    @property
    def value(self):
        return self._value

    @property
    def label(self):
        return self._label

    def __eq__(self, other):
        return self._value == other


class BChoicesMeta(type):
    def __new__(cls, name, bases, attrs):

        fields = {}  # {<name>:<BItem>}

        parents = [b for b in bases if isinstance(b, BChoicesMeta)]
        for kls in parents:
            for field_name in kls._fields:
                fields[field_name] = kls._fields[field_name]

        for k, v in attrs.items():
            if k.startswith('_'):
                continue
            if isinstance(v, BItem):
                fields[k] = v
            elif isinstance(v, (tuple, list)) and len(v) == 2:
                fields[k] = BItem(v[0], v[1])
            elif isinstance(v, (int, float, str, bytes)):
                fields[k] = BItem(v, k.lower())

        # FIXME unordered dict for python3.5

        fields = OrderedDict(sorted(fields.items(), key=lambda x: x[1].order))
        for field_name, item in fields.items():
            attrs[field_name] = item

        new_cls = super().__new__(cls, name, bases, attrs)
        new_cls._fields = fields
        return new_cls

    @property
    def fields(cls):
        return cls._fields

    @property
    def choices(cls):
        return [(item.value, item.label) for _, item in cls.fields.items()]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def display_lookup(cls):
        return {value: label for value, label in cls.choices}

    def get_value_display(cls, item):
        return cls.display_lookup.get(item)

    def __getattr__(self, item):
        if item in self.fields:
            return self.fields[item]
        return super().__getattr__(item)

    def __contains__(self, item):
        return item in self.values

    def __iter__(self):
        for item in self.choices:
            yield item

    def __len__(self):
        return len(self.choices)


class BChoices(metaclass=BChoicesMeta):
    pass
