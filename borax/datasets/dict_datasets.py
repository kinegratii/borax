# coding=utf8


class DictDataset:
    def __init__(self, data, primary_field=None):
        self._data = []
        if data:
            self._data = list(data)
        self._primary_field = primary_field

    @property
    def data(self):
        return self._data

    def __iter__(self):
        for item in self.data:
            yield item
