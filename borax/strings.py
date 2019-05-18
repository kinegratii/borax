# coding=utf8
import re
import html

from django.utils.html import mark_safe


def camel2snake(s):
    camel_to_snake_regex = r'((?<=[a-z0-9])[A-Z]|(?!^)(?<!_)[A-Z](?=[a-z]))'
    return re.sub(camel_to_snake_regex, r'_\1', s).lower()


def snake2camel(s):
    snake_to_camel_regex = r"(?:^|_)(.)"
    return re.sub(snake_to_camel_regex, lambda m: m.group(1).upper(), s)


def get_percentage_display(value, places=2):
    fmt = '{0:. f}%'.replace(' ', str(places))
    return fmt.format(value * 100)


def _escape(s):
    if hasattr(s, '__html__'):
        return s.__html__()
    return SafeString(html.escape(str(s)))


class SafeString(str):
    """Implement __html__ protocol for str class.inspired by SafeData in django and Markup in jinja2.
    """
    def __new__(cls, base=u'', encoding=None, errors='strict'):
        if hasattr(base, '__html__'):
            base = base.__html__()
        if encoding is None:
            return str.__new__(cls, base)
        return str.__new__(cls, base, encoding, errors)

    def __html__(self):
        return self

    @classmethod
    def escape(cls, s):
        rv = _escape(s)
        if rv.__class__ is not cls:
            return cls(rv)
        return rv
