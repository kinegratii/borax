# coding=utf8

import operator

__all__ = ['join_one', 'join', 'old_join_one', 'old_join']


def join_one(ldata, rdata, on, select_as, default=None):
    if isinstance(rdata, (list, tuple)):
        rdata = dict(rdata)
    if not isinstance(rdata, dict):
        raise TypeError("Unsupported Type for values param.")

    if isinstance(on, str):
        lic = operator.itemgetter(on)
    elif callable(on):
        lic = on
    else:
        raise TypeError('str or callable only supported for on param. ')

    for litem in ldata:
        if not (isinstance(on, str) and on not in litem):
            lv = lic(litem)
            rvv = rdata.get(lv, default)
            litem[select_as] = rvv
    return ldata


CLAUSE_SINGLE_TYPES = (str, tuple)


class OnClause(tuple):
    def __new__(self, lkey, rkey=None):
        rkey = rkey or lkey
        return tuple.__new__(OnClause, (lkey, rkey))

    @classmethod
    def from_val(cls, val):
        cm = val.__class__.__name__
        if cm == "OnClause":
            return val
        elif cm == "str":
            return cls(val, val)
        elif cm == "tuple":
            return cls(*val[:2])
        else:
            raise TypeError("Cannot build OnClause from a {} object.".format(cm))


class SelectClause(tuple):
    def __new__(self, rkey, lkey=None, default=None):
        lkey = lkey or rkey
        return tuple().__new__(SelectClause, (rkey, lkey, default))

    @classmethod
    def from_val(cls, val):
        cm = val.__class__.__name__
        if cm == "SelectClause":
            return val
        elif cm == "str":
            return cls(val, val, None)
        elif cm == "tuple":
            return cls(*val[:3])
        else:
            raise TypeError("Cannot build SelectClause from a {} object.".format(cm))


OC = OnClause
SC = SelectClause


def join(ldata, rdata, on, select_as):
    if isinstance(on, CLAUSE_SINGLE_TYPES):
        on = [on]
    if isinstance(on, list):
        lfields, rfields = zip(*list(map(OnClause.from_val, on)))

        def on_callback(_li, _ri):
            return operator.itemgetter(*lfields)(_li) == operator.itemgetter(*rfields)(_ri)
    elif callable(on):
        on_callback = on
    else:
        raise TypeError('str or callable only supported for on param. ')

    if isinstance(select_as, CLAUSE_SINGLE_TYPES):
        select_as = [select_as]
    sf_list = list(map(SelectClause.from_val, select_as))

    def _pick_data(_item, _sfs):
        result = {}
        for rk, lk, defv in _sfs:
            result[lk] = _item.get(rk, defv)
        return result

    for litem in ldata:
        for ritem in rdata:
            if on_callback(litem, ritem):
                _ri = ritem
                break
        else:
            _ri = {}
        litem.update(_pick_data(_ri, sf_list))
    return ldata


def old_join_one(data_list, values, from_, as_, default=None):
    if isinstance(values, (list, tuple)):
        values = dict(values)
    if not isinstance(values, dict):
        raise TypeError("Unsupported Type for values param.")
    for item in data_list:
        if from_ in item:
            val = item[from_]
            if val in values:
                ref_val = values[val]
            else:
                ref_val = default
            item[as_] = ref_val
    return data_list


def old_join(data_list, values, from_, to_, as_args=None, as_kwargs=None):
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
