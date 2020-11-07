# join 模块

> 模块 `borax.datasets.join_`

> Changed in v3.2.0

## 重要说明

### Changed in v3.4.0 : 函数传参方式

在 v3.4.0 新增 `deep_join` 和 `deep_join_one` 两个函数，这两个函数对第一个参数 `ldata` 使用 赋值传参方式。

| 传参方式 | 函数                     |
| -------- | ------------------------ |
| 引用传参 | join_one, join           |
| 赋值传参 | deep_join_one, deep_join |

### Changed in v3.2.0

从v3.2.0开始，我们重写 `join` 和 `join_one` ，原有的函数分别重命名为 `old_join` 和 `old_join_one` ，主要变化如下：

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

本模块实现了类似于数据库的 LEFT JOIN 数据列表操作，从另一个数据集获取某一个或几个列的值，加到当前数据集中。

> **关于LEFT JOIN** ：LEFT JOIN返回左表的全部行和右表满足ON条件的行，如果左表的行在右表中没有匹配，那么这一行右表中对应数据用NULL代替。

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

## 配置类

`join_` 模块定义了两个配置类，分别用于定义 `join` 函数的 `on` 和 `select_as` 参数。

- `OC` 是 `OnClause` 的类别名，`SC` 是 `SelectClause` 的类别名。
- OnClause和SelectClause均继承自 tuple 。
- `from_val` 类方法可以将一个标准类型（包括 str、tuple，不支持list）的对象转化成对应的 Clause 类。

### OnClause/OC

*`OnClause(lkey, rkey=None)`*

表示 on 表达式的条件，一个 `OnClause` 表示一个等值条件。

- lkey：条件的左值字段。
- rkey：条件的右值字段。

### SelectClause/SC

*`SelectClause(rkey, lkey=None, default=None)`*

表示 select表达式的字段定义，一个 `SelectClause` 表示一个字段。

- rkey：右边数据的字段。
- lkey：加入左边数据的命名的命名字段，如果不提供，默认和 rkey一致。
- default：在右边数据找不到时使用该默认值。

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

*`join(ldata, rdata, on, select_as)`*

实现左、右数据集的连接。

| 参数      | 类型                      | 说明                             |
| --------- | ------------------------- | -------------------------------- |
| ldata     | List[Dict]                | 左边数据集                       |
| rdata     | List[Dict]                | 右边数据集                       |
| on        | List[OnClause] / callback | 使用左边的连接字段，支持回调函数 |
| select_as | str / List[SelectClause]  | 右边数据在结果的字段名称         |

备注：

- 和 `join` 相比，没有显式的 defaults 参数，默认值可以在 `select_as` 参数中配置。

#### on参数

on支持以下几种参数方式：

- 回调函数。定义如下 ，返回是否匹配。

```python
def on_callback(litem:dict, ritem:dict) -> bool:
    pass
```

注意：如果在右边数据有多条记录匹配时，只会使用第一次成功匹配的记录。

- 标准配置：当 `on` 为字段配置时，其类型为 `List[OnClause]`。 该定义了一个由若干个 OnClause 对象组成的列表。注意这里的列表（list）不能使用元组（tuple）代替。通用格式如下：

```python
  [
     OnClause('lkey1', 'rkey1'),
     OnClause('lkey2', 'rkey2'),
      # ...
  ]
```

  对应的条件表达式为  `left_item.lkey1 == right_item.rkey1 and left_item.lkey2==right_item.rkey2`。

- 简易配置。当含有以下条件时，可以不显式定义 `OnClause` 对象，由程序自动转化为对应的 `OnClause`对象，。

   (1) 当某一个等值条件左右两边的key相同。

   (2) 只有一个等值条件，可以省略外面的 `[]` 列表符号。

```python
# 以下三种方式是相同的。
on = [('x', 'x'), ('y', 'y')]
on = ['x', 'y']
on = [OnClause('x', 'x'), OnClause('y', 'y')]

# 以下三种方式是等效的。
on = 'x'
on = OnClause('x', 'x')
on = [OnClause('x', 'x')]
```

下列的三种方式也是等效的，注意和上面 `on = ['x', 'y']` 的区别。

```python
on = （'x', 'y'）
on = OnClause('x', 'y')
on = [OnClause('x', 'y')]
```

#### select_as参数

- 标准配置：其类型为 `List[SelectClause]`。 该定义了一个由若干个 SelectClause 对象组成的列表。注意这里的列表（list）不能使用元组（tuple）代替。通用格式如下：

```python
[
    SelectClause(<right_key>, <left_key>, <default_value>),
    SelectClause(<right_key>, <left_key>, # 省略默认值
    SelectClause <right_key>,),
 ]
```

元组元素的三个值分别表示右边数据字段名称、左边数据字段名称、默认值。和 `on` 参数类似，也可以依次省略后面两个内容。

- 简易配置。当含有以下条件时，可以不显式定义 `SelectClause` 对象，由程序自动转化为对应的 `SelectClause`对象。

 (1) 当某一个选择条件lkey和default使用默认值时。

 (2) 只有一个选择条件，可以省略外面的 `[]` 列表符号。

### deep_join_one

*`deep_join_one(ldata, rdata, on, select_as, default=None)`*

同 `join_one` ，但 `ldata` 采用 赋值传参方式。

### deep_join

*`deep_join(ldata, rdata, on, select_as)`*

同 `join` ，但 `ldata` 采用 赋值传参方式。

## 旧版API


### old_join_one

*`old_join_one(data_list, values, from_, as_, default=None)`*

> v3.1 新增default参数。

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



