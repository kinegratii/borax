# coding=utf8

import operator


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


def _sf(val):
    """Build a SelectField from val
    """
    if isinstance(val, str):
        return val, val, None
    elif isinstance(val, (list, tuple)):
        l = len(val)
        if l == 1:
            return val[0], val[0], None
        elif l == 2:
            return val[0], val[1], None
        else:
            return tuple(val[0:3])


def _parse_on(val):
    if isinstance(val, str):
        return (val, val),
    if isinstance(val, (list, tuple)):
        def _ep(_v):
            if isinstance(_v, str):
                return _v, _v
            else:
                return _v

        return tuple(map(_ep, val))


def join(ldata, rdata, on, select_as):
    if isinstance(on, (list, tuple, str)):
        lfields, rfields = zip(*_parse_on(on))
        on_callback = lambda _li, _ri: operator.itemgetter(*lfields)(_li) == operator.itemgetter(*rfields)(_ri)
    elif callable(on):
        on_callback = on
    else:
        raise TypeError('str or callable only supported for on param. ')

    if isinstance(select_as, str):
        select_as = select_as,
    sf_list = list(map(_sf, select_as))

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
