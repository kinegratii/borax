# Fetch 模块

> 模块：`borax.datasets.fetch` 

## 函数接口

`borax.datasets.fetch` 模块实现了从数据列表按照指定的一个或多个属性/键选取数据。

`fetch` 模块包含了以下几个函数：

- `fetch(iterable, key, *keys, default=EMPTY, defaults=None, getter=None)`
- `ifetch(iterable, key, *keys, default=EMPTY, defaults=None, getter=None)`
- `fetch_single(iterable, key, default=EMPTY, getter=None)`
- `ifetch_multiple(iterable, *keys, defaults=None, getter=None)`
- `ifetch_single(iterable, key, default=EMPTY, getter=None)`

各个参数意义如下：

- iterable：数据列表
- key / keys：键值、属性访问方式的索引
- default：默认值，用于选择单个属性
- defaults：默认值字典，用于选择多个属性
- getter：自定义访问回调函数

通常使用 `fetch` 函数即可。

## 基本使用

### 选取单个属性

从 `objects` 数据获取 `name` 的数据。

```python
from borax.datasets.fetch import fetch

objects = [
    {'id': 282, 'name': 'Alice', 'age': 30},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56},
]

names = fetch(objects, 'name')
print(names)
```

输出

```
['Alice', 'Bob', 'Charlie']
```

### 选取多个属性

从 `objects` 数据获取 `name` 和 `age` 的数据。

```python
from borax.datasets.fetch import fetch

objects = [
    {'id': 282, 'name': 'Alice', 'age': 30},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56},
]

names, ages = fetch(objects, 'name', 'age')
print(names)
print(ages)
```

输出

```
['Alice', 'Bob', 'Charlie']
[30, 56, 56]
```

### 列表型数据

`fetch` 函数第一个参数 `iterable` 也可以是列表型数据。

```python
from borax.datasets.fetch import fetch

data = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
]
zeros, twos = fetch(data, 0, 2)
print(zeros)
print(twos)
```

输出

```
[0, 10, 20]
[2, 12, 22]
```

此时情况下和 `zip` 函数有相类似的功能，上述例子可改写如下：

```python
data = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
]
zeros, _, twos, *_ = zip(*data)
print(zeros)
print(twos)
```



## 提供默认值

当 `iterable` 数据列表缺少某个属性/键，可以通过指定 `default` 或 `defaults` 参数提供默认值。

```python
from borax.datasets.fetch import fetch

objects = [
    {'id': 282, 'name': 'Alice', 'age': 30, 'gender': 'female'},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'gender': 'male'},
]

print('Demo for one default value')
genders = fetch(objects, 'gender', default='unknown')
print(genders)

print('Demo for multiple default values')
ages, genders = fetch(objects, 'age', 'gender', defaults={'age': 0, 'gender':'unknown'})
print(genders)
print(ages)
```

结果输出

```
Demo for one default value
['female', 'unknown', 'male']
Demo for multiple default values
['female', 'unknown', 'male']
[30, 56, 0]
```

## 属性访问


除了上述的键值访问方式，`fetch` 函数还内置属性访问的获取方式。

```python
from borax.datasets.fetch import fetch

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


points = [
    Point(1, 2, 3),
    Point(4, 5, 6),
    Point(7, 8, 9)
]

print('Fetch x values:')
x = fetch(points, 'x')
print(x)

print('Fetch x,y,z values:')
x, y, z = fetch(points, 'x', 'y', 'z')
print(x)
print(y)
print(z)
```

结果输出

```
Fetch x values:
[1, 4, 7]
Fetch x,y,z values:
[1, 4, 7]
[2, 5, 8]
[3, 6, 9]
```

## 自定义Getter

除了内置的属性访问方式 [itemgetter](https://docs.python.org/3.6/library/operator.html#operator.itemgetter) 和键值访问方式 [attrgetter](https://docs.python.org/3.6/library/operator.html#operator.attrgetter) 外，`fetch` 函数还通过 `getter` 参数支持自定义访问方式。

getter 需满足下列的几个条件：

- 是一个函数，命名函数或匿名函数均可
- 该函数必须含有 *item* 和 *key* 两个参数
- 返回是具体的数值

例子：

```python
from borax.datasets.fetch import fetch


class Point:
    def __init__(self, index, x, y, z):
        self.index = index
        self._data = {'x': x, 'y': y, 'z': z}

    def get(self, key):
        return self._data.get(key)


points = [
    Point('a', 1, 2, 3),
    Point('b', 4, 5, 6),
    Point('c', 7, 8, 9)
]


def point_getter(item, key):
    return item.get(key)


print('Fetch x values:')
x = fetch(points, 'x', getter=point_getter)
print(x)

print('Fetch x,y,z values:')
x, y, z = fetch(points, 'x', 'y', 'z', getter=point_getter)
print(x)
print(y)
print(z)
```


结果输出

```
Fetch x values:
[1, 4, 7]
Fetch x,y,z values:
[1, 4, 7]
[2, 5, 8]
[3, 6, 9]
```

需要注意的是，自定义 Getter 是应用至所有属性的，内置的 *属性访问方式* 和 *键值访问方式* 将不再使用，混用将可能无法获得期望的结果。

错误的示例1

```bash
>>> indexes, xs = fetch(points, 'index', 'x', getter=point_getter)
[None, None, None]
[1, 4, 7]
```

错误的示例2

```bash
>>> indexes, xs = fetch(points, 'index', 'x')
Traceback (most recent call last):
TypeError: 'Point' object is not subscriptable
```

应当分别调用 `fetch` 函数。

正确的用法

```python
x, y = fetch(points, 'x', 'y', getter=point_getter)

print(x)
print(y)

indexes = fetch(points, 'index')
print(indexes)
```

结果输出

```
[1, 4, 7]
[2, 5, 8]
['a', 'b', 'c']
```