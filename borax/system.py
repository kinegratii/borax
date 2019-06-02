# coding=utf8
import os
import sys
from datetime import datetime


def load_class(s):
    """Import a class
    :param s: the full path of the class
    :return:
    """
    path, class_ = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, class_)


def check_path_variables(execute_filename):
    try:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
    except KeyError:
        user_paths = []
    for item in user_paths:
        if os.path.exists(os.path.join(item, execute_filename)):
            return True
    os_paths_list = os.environ['PATH'].split(';')
    for item in os_paths_list:
        if os.path.exists(os.path.join(item, execute_filename)):
            return True
    return False


SUFFIX_DT = '%Y%m%d%H%M%S'
SUFFIX_DT_UNDERLINE = '%Y_%m_%d_%H_%M_%S'
SUFFIX_DATE = '%Y%m%d'
SUFFIX_DATE_UNDERLINE = '%Y_%m_%d'


def rotate_filename(filename: str, time_fmt: str = SUFFIX_DT, sep: str = '_', now=None, **kwargs):
    """ Rotate filename or filepath with datetime string as suffix.
    :param filename:
    :param time_fmt:
    :param sep:
    :param now:
    :param kwargs:
    :return:
    """
    now = now or datetime.now()
    kwargs.update({'now': now})
    actual_path = filename.format(**kwargs)
    s1, s2 = os.path.splitext(actual_path)
    return ''.join([s1, sep, now.strftime(time_fmt), s2])
