# coding=utf8

import collections


class TableLookup:
    def __init__(self, fields, primary=None):
        self._fields = fields
        self._item_class = collections.namedtuple('Item', fields)
        self._dataset = collections.OrderedDict()
        if primary:
            self.primary = primary
            self._primary_index = fields.index(primary)
        else:
            self.primary = fields[0]
            self._primary_index = 0

    def feed(self, table_data):
        for data_item in table_data:
            self._dataset.update({
                data_item[self._primary_index]: self._item_class(*data_item)
            })
        return self

    def find(self, key, default=None):
        return self._dataset.get(key, default)

    def select_as_dict(self, field):
        return {k: getattr(v, field) for k, v in self._dataset.items()}

    def __iter__(self):
        for item in self._dataset.values():
            yield item
