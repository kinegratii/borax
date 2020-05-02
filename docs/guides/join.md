# join 模块

> 模块 `borax.datasets.join_`

> Changed in V3.2.0

## 重要说明

从V3.2.0开始，我们重写 `join` 和 `join_one` ，原有的函数分别重命名为 `old_join` 和 `old_join_one` ，主要变化：

- 使用符合SQL的参数命名，比如 on、select_as 等。
- 原有比较分散的参数进行合并。
- 支持回调函数。

如果不想使用新版本API，将下面的引入语句

```python
from borax.datasets.join_ import join, join_one
```

修改为

```python
from borax.datasets.join_ import old_join as join, old_join_one as join_one
```

如果想将旧API修改新的API，请参见下面的 *使用迁移* 一节。

## 概述

本模块实现了类似于数据库的 JOIN 数据列表操作，从另一个数据集获取某一个或几个列的值。

> 本模块的 *join_* 函数将会修改传入的列表数据，如需不影响原有数据，可以提前复制一份数据。

本模块示例所用的数据描述如下：

图书清单

```python
books = [
    {'name': 'Python入门教程', 'catalog': 1, 'price': 45},
    {'name': 'Java标准库', 'catalog': 2, 'price': 80},
    {'name': '软件工程(本科教学版)', 'catalog': 3, 'price': 45},
    {'name': 'Django Book', 'catalog': 1, 'price': 45},
    {'name': '系统架构设计教程', 'catalog': 3, 'price': 104},
]
```

类别（字典格式）

```python
catalogs_dict = {
    1: 'Python',
    2: 'Java',
    3: '软件工程'
}
```

类别（列表格式）

```python
catalogs_list = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Java'},
    {'id': 3, 'name': '软件工程'},
]
```

## API

### join_one

*`join_one(ldata, rdata, on, select_as, default=None)`*

从右边数据获取一个字段的值，加到左边数据集。

各参数定义如下：

| 参数      | 类型           | 说明                             |
| --------- | -------------- | -------------------------------- |
| ldata     | List[Dict]     | 左边数据集                       |
| rdata     | Dict / List    | 右边数据集                       |
| on        | str / callable | 使用左边的连接字段，支持回调函数 |
| select_as | str            | 右边数据在结果的字段名称         |
| default   | Any            | 右边数据集找不到时的默认值       |

备注：

- `rdata`：该参数标准类型为 `Dict` 。但同时也支持 `List` ，Borax 将使用 `dict(list_obj)`  的方式进行转化。

- 当 `on` 参数为函数时，接收 `litem` 参数，表示左边数据集的当前记录，返回连接值。当 `on` 为字符串时，Borax 将其转化为对应的函数。

```python
# 以下两种定义方式是等效的
on = 'catalog'

def on(litem):
    return litem['catalog']
```

在例子中，实现从 `catalog_dict` 将书本类别名称加到 `books` ，可以使用以下的定义方式。

```python
join_one(books, catalog_dict, on='catalog', select_as='catalog_name')
```



### join

*`join(ldata, rdata, on, select_as, defaults=None)`*

实现左、右数据集的连接。

| 参数      | 类型                                      | 说明                             |
| --------- | ----------------------------------------- | -------------------------------- |
| ldata     | List[Dict]                                | 左边数据集                       |
| rdata     | List[Dict]                                | 右边数据集                       |
| on        | str / Tuple[Union[str, tuple]] / Callable | 使用左边的连接字段，支持回调函数 |
| select_as | str                                       | 右边数据在结果的字段名称         |
| default   | Any                                       | 右边数据集找不到时的默认值       |

备注：

- 当`on` 参数为函数时，定义如下 ，返回是否匹配。

```python
def on_callback(litem:dict, ritem:dict) -> bool:
    pass
```

- 当 `on` 为字段配置时，其类型为 `Tuple[Union[str, Tuple]]`。 该定义了一个元组，元组的每个元素又是由2个字符串组成的元组。通用格式如下：

```python
  (
      (<left_item.key1>, <right_item.key1>),
      (<left_item.key2>, <right_item.key2>),
      # ...
  )
```

  表示 `left_item.key1=right.item.key1&left_item.key2=right.item.key2`。

当某一个条件左右两边的key相同时，内部的元组可以省略为一个字符串。

```python
# 以下两种方式是相同的。
on = (('x', 'x'), ('y', 'y'))

on = ('x', 'y')
```

当只有一个条件时，还可以继续省略外层的元组，只定义一个字符串即可。以下三种是等效的。

```python
on = 'x'
on = ('x',)
on = (('x', 'x'),)
```






### old_join_one

*`old_join_one(data_list, values, from_, as_, default=None)`*

> V3.1 新增default参数。

从字典读取某一列的值。

从 `catalogs_dict` 获取类别名称并按照 catalogs.id 分组填充至 `books` 。

```python
catalog_books = old_join_one(books, catalogs_dict, from_='catalog', as_='catalog_name')
```

输出

```python
[
    {'name': 'Python入门教程', 'catalog': 1, 'price': 45, 'catalog_name': 'Python'},
    {'name': 'Java标准库', 'catalog': 2, 'price': 80, 'catalog_name': 'Java'},
    {'name': '软件工程(本科教学版)', 'catalog': 3, 'price': 45, 'catalog_name': '软件工程'},
    {'name': 'Django Book', 'catalog': 1, 'price': 45, 'catalog_name': 'Python'},
    {'name': '系统架构设计教程', 'catalog': 3, 'price': 104, 'catalog_name': '软件工程'}
]
```



### old_join

*`old_join(data_list, values, from_, to_, as_args=None, as_kwargs=None):`*

从字典读取多个列的值。

示例1

```python
catalog_books = old_join(
    books,
    catalogs_list,
    from_='catalog',
    to_='id',
    as_kwargs={'name': 'catalog_name'}
)
```

输出

```python
[
    {'name': 'Python入门教程', 'catalog': 1, 'price': 45, 'catalog_name': 'Python'},
    {'name': 'Java标准库', 'catalog': 2, 'price': 80, 'catalog_name': 'Java'},
    {'name': '软件工程(本科教学版)', 'catalog': 3, 'price': 45, 'catalog_name': '软件工程'},
    {'name': 'Django Book', 'catalog': 1, 'price': 45, 'catalog_name': 'Python'},
    {'name': '系统架构设计教程', 'catalog': 3, 'price': 104, 'catalog_name': '软件工程'}
]
```

## 使用示例

使用示例

```python
points = [
    {'x': 1, 'y': 1, 'val': 34},
    {'x': 2, 'y': 2, 'val': 34},
    {'x': 4, 'y': 4, 'val': 34},
]

links = [
    {'x': 1, 'y': 1, 'val': 56, 'link1': 23, 'link2': 102},
    {'x': 2, 'y': 2, 'val': 78, 'link1': 45, 'link2': 345},
    {'x': 3, 'y': 4, 'val': 25, 'link1': 90, 'link2': 456},
]
```

## 使用迁移

### 迁移join_one

`join_one` 函数迁移比较简单，只需要参数重命名即可。

- `from_` 改为 `on` 
- `as_` 改为 `select_as`

如果调用时不使用关键字方式，可以不作任何改变。

### 迁移join

第一步，原有的 `from_` 和 `to_` 合并为 `on` 参数，只要把旧版的两个参数合并为一个元组，传给 `on`。

如果`from_` 和 `to_` 是一样的，只要将该字符串传给 `on` 即可。

```python
old_join(from_'foo', to_='bar')
# 转化为
join(on=('foo','bar'))

old_join(from_'foo', to_='foo')
# 转化为
join(on='foo')
```

第二步， `as_args` 和 `as_kwargs` 合并为 `select_as` ，转化方式如下：

```python
<select_as> = <as_args> + <as_kwargs>.items()
```

例如：

```python
old_join(as_args=['Xxx', 'Yyy'], as_kwargs={'Zzz':'cZzz', 'Www':'cWww'})
join(select_as=(
    'Xxx',
    'Yyy',
    ('Zzz', 'cZzz'),
    ('Www', 'cWww')
))
```


