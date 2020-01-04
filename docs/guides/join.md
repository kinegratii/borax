# join 模块

> 模块 `borax.datasets.join_`

本模块实现了类似于数据库的 JOIN 数据列表操作，从另一个数据集获取某一个或几个列的值。

## 概述

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




## join_one方法

*`join_one(data_list, values, from_, as_, default=None)`*

> V3.1 新增default参数。

从字典读取某一列的值。

从 `catalogs_dict` 获取类别名称并按照 catalogs.id 分组填充至 `books` 。

```python
catalog_books = join_one(books, catalogs_dict, from_='catalog', as_='catalog_name')
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



## join方法

*`join(data_list, values, from_, to_, as_args=None, as_kwargs=None):`*

从字典读取多个列的值。

示例1

```python
catalog_books = join(
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

