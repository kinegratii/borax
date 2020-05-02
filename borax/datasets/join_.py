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
