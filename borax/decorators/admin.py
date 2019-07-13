# coding=utf8
import warnings

__all__ = ['attr', 'admin_action', 'action', 'display_field']

warnings.warn('This module is deprecated, use nickel.admin_utils.decorators instead.', DeprecationWarning)


def attr(**kwargs):
    def _inner(fun):
        for name, value in kwargs.items():
            setattr(fun, name, value)
        return fun

    return _inner


def admin_action(short_description=None, allowed_permissions=None, **kwargs):
    if allowed_permissions is not None:
        kwargs.update({'allowed_permissions': allowed_permissions})
    return attr(short_description=short_description, **kwargs)


# Old name alias
action = admin_action


def display_field(short_description, admin_order_field=None, **kwargs):
    if admin_order_field is not None:
        kwargs.update({'admin_order_field': admin_order_field})
    return attr(short_description=short_description, **kwargs)
