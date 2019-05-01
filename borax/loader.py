# coding=utf8

import warnings

from .system import load_class as _load_class


def load_class(s):
    """Import a class
    :param s: the full path of the class
    :return:
    """
    warnings.warn('This method is deprecated. Use `borax.system.load_class` instead .', DeprecationWarning)
    return _load_class(s)
