# coding=utf8


from collections import OrderedDict

__all__ = ['Item', 'ConstChoices']


class Item:
    _order = 0

    def __init__(self, value, display=None, order=None):
        self.value = value
        self.display = display
        if order is None:
            Item._order += 1
            self.order = Item._order
        else:
            self.order = order


class ChoicesMetaclass(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, attrs):

        choices = []
        display_lookup = {}

        fields = {}

        for k, v in attrs.items():
            if k.startswith('_'):
                continue
            if isinstance(v, Item):
                fields[k] = v
            elif isinstance(v, (tuple, list)) and len(v) == 2:
                fields[k] = Item(value=v[0], display=v[1])
            else:
                fields[k] = Item(value=v, display=v)

        fields = OrderedDict(sorted(fields.items(), key=lambda x: x[1].order))

        for field_name in fields:
            val_item = fields[field_name]
            choices.append((val_item.value, val_item.display))
            display_lookup[val_item.value] = val_item.display
            attrs[field_name] = val_item.value

        attrs['_fields'] = fields
        attrs['choices'] = choices
        attrs['display_lookup'] = display_lookup
        return type.__new__(cls, name, bases, attrs)


class ConstChoices(metaclass=ChoicesMetaclass):
    @classmethod
    def is_valid(cls, value):
        return value in cls.display_lookup

    @classmethod
    def get_value_display(cls, value, default=None):
        return cls.display_lookup.get(value, default)
