import os
import sys
from datetime import datetime

from borax.constants import DatetimeFormat


def load_class(s):
    """Import a class
    :param s: the full path of the class
    :return:
    """
    path, class_ = s.rsplit('.', 1)
    __import__(path)
    mod = sys.modules[path]
    return getattr(mod, class_)


load_object = load_class  # Only a alias name.


def check_path_variables(execute_filename: str) -> bool:
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


# These constants has been deprecated.
SUFFIX_DT = '%Y%m%d%H%M%S'
SUFFIX_DT_UNDERLINE = '%Y_%m_%d_%H_%M_%S'
SUFFIX_DATE = '%Y%m%d'
SUFFIX_DATE_UNDERLINE = '%Y_%m_%d'


def rotate_filename(filename: str, time_fmt: str = DatetimeFormat.SUFFIX_DT, sep: str = '_', now=None, **kwargs) -> str:
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
