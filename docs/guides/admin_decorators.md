# decorators.admin 模块

> 模块： `borax.decorators.admin`

> 本模块已废弃，将在 v2.0 移除。

## attr

函数签名

```
attr(**kwargs)
```

设置函数对象的属性。

## display_field

函数签名

```
display_field(short_description, admin_order_field=None, **kwargs)
```

使用装饰器定义回调函数的 [list_display](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display) 。


原始例子：

```python
def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()
upper_case_name.short_description = 'Name'

class PersonAdmin(admin.ModelAdmin):
    list_display = (upper_case_name,)
```

使用 `@display_field` 改写如下：

```python
@display_field(short_description='Name')
def upper_case_name(obj):
    return ("%s %s" % (obj.first_name, obj.last_name)).upper()

class PersonAdmin(admin.ModelAdmin):
    list_display = (upper_case_name,)
```

## action

函数签名

```
action(short_description=None, allowed_permissions=None, **kwargs)
```

使用装饰器定义 [action](https://docs.djangoproject.com/en/2.0/ref/contrib/admin/actions/#writing-action-functions) 函数 。

例子：

```python
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Mark selected stories as published"
```

改写后：

```python
@action(short_description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
```