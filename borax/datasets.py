# coding=utf8


def join_one(data_list, values, from_, as_):
    if isinstance(values, (list, tuple)):
        values = dict(values)
    if not isinstance(values, dict):
        raise TypeError("Unsupported Type for values param.")
    for item in data_list:
        if from_ in item:
            val = item[from_]
            if val in values:
                ref_val = values[val]
                item[as_] = ref_val
    return data_list


def join(data_list, values, from_, to_, as_args=None, as_kwargs=None):
    as_args = as_args or []
    as_kwargs = as_kwargs or {}
    as_fields = {**{a: a for a in as_args}, **as_kwargs}
    dict_values = {v[to_]: v for v in values}
    for item in data_list:
        kv = item[from_]
        val_dic = dict_values[kv]
        for f1, f2 in as_fields.items():
            item[f2] = val_dic[f1]
    return data_list


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
