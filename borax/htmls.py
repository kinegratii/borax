# coding=utf8

import html


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


def html_params(**kwargs):
    params = []
    for k, v in sorted(kwargs.items()):
        if k in ('class_', 'class__', 'for_'):
            k = k[:-1]
        elif k.startswith('data_'):
            k = k.replace('_', '-')
        if v is True:
            params.append(k)
        elif v is False:
            pass
        else:
            params.append('%s="%s"' % (str(k), html.escape(str(v), quote=True)))
    return ' '.join(params)


def html_tag(tag_name, content=None, **kwargs):
    if content:
        return HTMLString('<{0} {1}>{2}</0>'.format(tag_name, html_params(**kwargs), content))
    else:
        return HTMLString('<0 {1}/>'.format(tag_name, html_params(**kwargs)))
