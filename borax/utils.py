import collections.abc
from functools import reduce


def _resolve_value(val, args=None, kwargs=None):
    if callable(val):
        args = args or []
        kwargs = kwargs or {}
        return val(*args, **kwargs)
    else:
        return val


def force_iterable(obj):
    if not isinstance(obj, collections.abc.Iterable) or isinstance(obj, str):
        return [obj]
    return obj


def safe_chain_getattr(obj, attr):
    """recourse through an attribute chain to get the ultimate value."""
    return reduce(getattr, attr.split('.'), obj)


def chain_getattr(obj, attr, value=None):
    """Get chain attribute for an object.
    """
    try:
        return _resolve_value(safe_chain_getattr(obj, attr))
    except AttributeError:
        return value


def get_item_cycle(data, index, start=0):
    """
    get_item_cycle(data, index) == list(itertools.cycle(data))[:index-start][-1]
    :param data:
    :param index:
    :param start:
    :return:
    """
    length = len(data)
    return data[((index - start) % length + length) % length]


def firstof(iterable, func=None, default=None):
    for param in iterable:
        if callable(func):
            r = func(param)
        else:
            r = param
        if r:
            return r
    return default


def trim_iterable(iterable, limit, *, split=None, prefix='', postfix=''):
    """trim the list to make total length no more than limit.If split specified,a string is return.
    :return:
    """
    if split is None:
        sl = 0
        join = False
    else:
        sl = len(split)
        join = True
    result = []
    rl = 0
    for element in iterable:
        element = prefix + element + postfix
        el = len(element)
        if len(result) > 0:
            el += sl
        rl += el
        if rl <= limit:
            result.append(element)
        else:
            break
    if join:
        result = split.join(result)
    return result


def chunks(iterable, n):
    """Yield successive n-sized chunks from iterable object. https://stackoverflow.com/a/312464 """
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]


def flatten(iterable):
    """flat a iterable. https://stackoverflow.com/a/2158532
    """
    for el in iterable:
        if isinstance(el, collections.abc.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


def force_list(val, sep=','):
    if isinstance(val, (list, set, tuple)):
        return tuple(val)
    elif isinstance(val, str):
        return tuple(val.split(sep))
    else:
        return val,
