import html
from typing import Dict, List, Union


def _escape(s):
    if hasattr(s, '__html__'):
        return s.__html__()
    return HTMLString(html.escape(str(s)))


class HTMLString(str):
    """Implement __html__ protocol for str class.inspired by SafeData in django and Markup in jinja2.
    """

    def __new__(cls, base='', encoding=None, errors='strict'):
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
        if k in ('class_', 'for_', 'id_'):
            k = k[:-1]
        elif k.startswith('data_'):
            k = k.replace('_', '-')
        if v is True:
            params.append(k)
        elif v is False:
            pass
        elif isinstance(v, dict):
            v = {k_: v_ for k_, v_ in v.items() if v_ not in (None, '', [], ())}
            vs = ''.join([f'{k}:{v};' for k, v in v.items()])
            params.append(f'{k}="{vs}"')
        elif isinstance(v, list):
            vs = ' '.join(map(str, v))
            params.append(f'{k}="{vs}"')
        else:
            vs = html.escape(str(v), quote=True)
            params.append(f'{k}="{vs}"')
    return ' '.join(params)


SINGLE_TAGS = ('br', 'hr', 'img', 'input', 'param', 'meta', 'link')


def html_tag(tag_name: str, content: str = None,
             *, id_: str = None, style: Dict = None, class_: Union[List, str, None] = None, style_width: str = None,
             style_height: str = None, **kwargs) -> HTMLString:
    """Generate a HTML-safe string for a html element."""
    kw = {}
    if id_:
        kw['id_'] = id_
    style = style or {}
    if style_width is not None:
        style.update({'width': style_width})
    if style_height is not None:
        style.update({'height': style_height})
    if style:
        kw['style'] = style
    class_ = class_ or []
    if class_:
        kw['class_'] = class_
    kw.update(kwargs)
    if tag_name in SINGLE_TAGS:
        return HTMLString(f'<{tag_name} {html_params(**kw)}>')
    else:
        content = content or ''
        return HTMLString(f'<{tag_name} {html_params(**kw)}>{content}</{tag_name}>')
