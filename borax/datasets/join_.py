import operator
import copy

__all__ = ['join_one', 'join']


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
            raise TypeError(f"Cannot build OnClause from a {cm} object.")


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
            raise TypeError(f"Cannot build SelectClause from a {cm} object.")


OC = OnClause
SC = SelectClause


def _pick_data(_item, _sfs):
    result = {}
    for rk, lk, defv in _sfs:
        result[lk] = _item.get(rk, defv)
    return result


def join(ldata, rdata, on, select_as, defaults=None):
    if isinstance(on, CLAUSE_SINGLE_TYPES):
        on = [on]
    if isinstance(on, list):
        lfields, rfields = zip(*list(map(OnClause.from_val, on)))

        def on_callback(_li, _ri):
            for _lf, _rf in zip(lfields, rfields):
                if _lf in _li and _rf in _ri:
                    if _li[_lf] != _ri[_rf]:
                        return False
                else:
                    return False
            else:
                return True

    elif callable(on):
        on_callback = on
    else:
        raise TypeError('str or callable only supported for on param. ')

    if isinstance(select_as, CLAUSE_SINGLE_TYPES):
        select_as = [select_as]
    sf_list = list(map(SelectClause.from_val, select_as))

    defaults = defaults or {}
    for litem in ldata:
        for ritem in rdata:
            if on_callback(litem, ritem):
                _ri = ritem
                break
        else:
            _ri = defaults
        litem.update(_pick_data(_ri, sf_list))
    return ldata


def deep_join_one(ldata, rdata, on, select_as, default=None):
    ldata = copy.deepcopy(ldata)
    return join_one(ldata, rdata, on, select_as, default=default)


def deep_join(ldata, rdata, on, select_as, defaults=None):
    ldata = copy.deepcopy(ldata)
    return join(ldata, rdata, on, select_as, defaults)
