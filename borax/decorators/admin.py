# coding=utf8

__all__ = ['attr', 'action', 'display_field']


def attr(**kwargs):
    def _inner(fun):
        for name, value in kwargs.items():
            setattr(fun, name, value)
        return fun

    return _inner


def action(short_description=None, allowed_permissions=None, **kwargs):
    return attr(short_description=short_description, allowed_permissions=allowed_permissions, **kwargs)


def display_field(short_description, admin_order_field=None, **kwargs):
    return attr(short_description=short_description, admin_order_field=admin_order_field, **kwargs)
