# coding=utf8


from collections import OrderedDict

__all__ = ['Item', 'ConstChoices']


class Item(tuple):
    counter = 0

    def __new__(cls, value, display=None):
        display = display or value
        return tuple.__new__(cls, (value, display))

    def __init__(self, value, display=None):
        super(Item, self).__init__()
        self.value = self[0]
        self.display = self[1]
        self.counter = Item.counter
        Item.counter += 1


class ChoicesMetaclass(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, attrs):
        choices = []
        display_lookup = {}

        for k, v in attrs.items():
            if not k.startswith('_'):
                if isinstance(v, Item):
                    item = v
                elif isinstance(v, (tuple, list)) and len(v) == 2:
                    item = Item(*v)
                else:
                    item = Item(v, v)
                choices.append(item)
                display_lookup[item.value] = item.display
                attrs[k] = item.value
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
