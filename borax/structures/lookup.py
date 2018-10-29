# coding=utf8

import collections


class TableLookup:
    def __init__(self, fields, primary=None):
        self._fields = fields
        self._item_class = collections.namedtuple('Item', fields)
        self._dataset = {}
        if primary:
            self.primary = primary
            self._primary_index = fields.find(primary)
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
