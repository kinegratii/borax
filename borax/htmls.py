# coding=utf8

import html
from typing import Dict, List, Optional, Union


def _escape(s):
    if hasattr(s, '__html__'):
        return s.__html__()
    return HTMLString(html.escape(str(s)))


class HTMLString(str):
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


def html_params(**kwargs) -> str:
    params = []
    for k, v in kwargs.items():
        if k in ('class_', 'class__', 'for_', 'id_'):
            k = k[:-1]
        elif k.startswith('data_'):
            k = k.replace('_', '-')
        if v is True:
            params.append(k)
        elif v is False:
            pass
        elif isinstance(v, dict):
            vs = ''.join(['{}:{};'.format(k, v) for k, v in v.items()])
            params.append('%s="%s"' % (str(k), vs))
        elif isinstance(v, list):
            vs = ' '.join(map(str, v))
            params.append('%s="%s"' % (str(k), vs))
        else:
            params.append('%s="%s"' % (str(k), html.escape(str(v), quote=True)))
    return ' '.join(params)


SINGLE_TAGS = ('br', 'hr', 'img', 'input', 'param', 'meta', 'link')


def html_tag(tag_name: str, content: str = None,
             *, id_: str = None, style: Dict = None, class_: Union[List, str, None] = None, **kwargs) -> HTMLString:
    """生成元素的html字符串"""
    kw = {}
    if id_:
        kw['id_'] = id_
    style = style or {}
    if style:
        kw['style'] = style
    class_ = class_ or []
    if class_:
        kw['class_'] = class_
    kw.update(kwargs)
    if tag_name in SINGLE_TAGS:
        return HTMLString('<{0} {1}>'.format(tag_name, html_params(**kw)))
    else:
        content = content or ''
        return HTMLString('<{0} {1}>{2}</{0}>'.format(tag_name, html_params(**kw), content))
