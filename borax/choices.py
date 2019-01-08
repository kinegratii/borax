# coding=utf8


from collections import OrderedDict

__all__ = ['Item', 'ConstChoices']


class Item:
    _order = 0

    def __init__(self, value, display=None, *, order=None):
        self.value = value
        if display is None:
            self.display = str(value)
        else:
            self.display = str(display)
        if order is None:
            Item._order += 1
            self.order = Item._order
        else:
            self.order = order


class ChoicesMetaclass(type):
    def __new__(cls, name, bases, attrs):

        choices = []
        display_lookup = {}

        fields = {}

        parents = [b for b in bases if isinstance(b, ChoicesMetaclass)]
        for kls in parents:
            for field_name in kls._fields:
                fields[field_name] = kls._fields[field_name]

        for k, v in attrs.items():
            if k.startswith('_'):
                continue
            if isinstance(v, Item):
                fields[k] = v
            elif isinstance(v, (tuple, list)) and len(v) == 2:
                fields[k] = Item(value=v[0], display=v[1])
            elif isinstance(v, (int, float, str, bytes)):
                fields[k] = Item(value=v, display=v)

        fields = OrderedDict(sorted(fields.items(), key=lambda x: x[1].order))

        for field_name in fields:
            val_item = fields[field_name]

            if isinstance(val_item, Item):
                choices.append((val_item.value, val_item.display))
                display_lookup[val_item.value] = val_item.display
                attrs[field_name] = val_item.value
            else:
                choices.append((field_name, val_item.choices))

        attrs['_fields'] = fields
        attrs['_choices'] = choices
        attrs['_display_lookup'] = display_lookup
        return type.__new__(cls, name, bases, attrs)

    @property
    def choices(self):
        return self._choices

    @property
    def display_lookup(self):
        return self._display_lookup

    def __iter__(self):
        for item in self.choices:
            yield item

    def __len__(self):
        return len(self.choices)


class ConstChoices(metaclass=ChoicesMetaclass):
    @classmethod
    def is_valid(cls, value):
        return value in cls.display_lookup

    @classmethod
    def get_value_display(cls, value, default=None):
        return cls.display_lookup.get(value, default)
