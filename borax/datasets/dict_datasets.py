# coding=utf8


from borax.datasets.join_ import join_one, join


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

    def join(self, values, from_, to_, as_args=None, as_kwargs=None):
        join(
            self._data,
            values=values,
            from_=from_,
            to_=to_,
            as_args=as_args,
            as_kwargs=as_kwargs,
        )
        return self

    def join_one(self, values, from_, as_):
        join_one(self._data, values=values, from_=from_, as_=as_)
        return self
