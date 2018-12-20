# coding=utf8

import sys


def load_class(s):
    """Import a class
    :param s: the full path of the class
    :return:
    """
    path, class_ = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, class_)
