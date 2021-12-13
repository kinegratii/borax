# 快速开始


## 安装

> 从 v3.5.1开始，安装包文件格式为 *borax-3.5.1-py3-none-any.whl*（移除py2标识）以区别于之前的 *borax-3.5.0-py2.py3-none-any.whl*。

可以通过以下两种方式安装 Borax ：

1) 使用 *pip* ：

```shell
$ pip install borax
```
2) 使用 [poetry](https://poetry.eustace.io/) 工具：

```shell
$ poetry add borax
```

## 导入

一般来说， 作为功能的代码基本组织形式，建议导入 包(Package) 和  模块(Module) 。

例如，导入 `choices`：

```python
from borax import choices

class OffsetChoices(choices.ConstChoices):
    up = choices.Item((0, -1), 'Up')
    down = choices.Item((0, 1), 'Down')
    left = choices.Item((-1, 0), 'Left')
    right = choices.Item((0, 1), 'Right')
```

在某些情况下，也可以直接导入模块的 类(Class) 或 变量(Variate)。

```python
from borax.patterns.lazy import LazyObject

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = LazyObject(Point,args=[1,2])
print(p.x)
```

## 函数

borax 库在函数定义和调用方面，尽可能按照 [PEP3102](https://www.python.org/dev/peps/pep-3102/) 声明函数参数，即某些参数必须以关键字形式传入参数。

```
borax.choices.Items(value, display=None, *, order=None)
```

## 类型标注

从 v1.2.0 开始，部分模块支持 [Typing Hint](https://docs.python.org/3/library/typing.html) 。