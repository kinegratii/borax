# 快速开始


## 安装

可以通过以下三种方式安装 Borax ：

1) 使用 *pip* ：

```shell
$ pip install borax
```
2) 使用 [poetry](https://poetry.eustace.io/) 工具：

```shell
$ poetry add borax
```

3) 使用开发代码

```shell
git clone https://github.com/kinegratii/borax.git
cd borax
python setup.py install
```

## 导入

一般来说， 作为功能的代码基本组织形式，建议导入 *包(Package)* 和 *模块(Module)* 。

例如，导入 `choices`：

```python
from borax import choices

class OffsetChoices(choices.ConstChoices):
    up = choices.Item((0, -1), 'Up')
    down = choices.Item((0, 1), 'Down')
    left = choices.Item((-1, 0), 'Left')
    right = choices.Item((0, 1), 'Right')
```

不建议使用以下导入方式

```python
from borax.choices import ConstChoices, Item

class OffsetChoices(ConstChoices):
    up = Item((0, -1), 'Up')
    down = Item((0, 1), 'Down')
    left = Item((-1, 0), 'Left')
    right = Item((0, 1), 'Right')
```

在某些情况下，也可以直接导入模块的 *类(Class)* 或 *变量(Variate)*。

```python
from borax.patterns.lazy import LazyObject

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = LazyObject(Point,args=[1,2])
print(p.x)
```

## 调用

borax 库在函数定义和调用方面，尽可能按照 [PEP3102](https://www.python.org/dev/peps/pep-3102/) 声明函数参数，即某些参数必须以关键字形式传入参数。