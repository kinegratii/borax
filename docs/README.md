# Borax - python3工具库 - 中国农历/中文数字/设计模式/树形结构


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
![Python package](https://github.com/kinegratii/borax/workflows/Python%20package/badge.svg)
![Codecov](https://codecov.io/github/kinegratii/borax/coverage.svg)
![GitHub license](https://img.shields.io/github/license/kinegratii/borax)
[![borax](https://snyk.io/advisor/python/borax/badge.svg)](https://snyk.io/advisor/python/borax)



Borax 是一个Python3工具集合库。

本文档的所有内容都是基于最新版本，函数和类签名的变化参见各自的文档说明。

本项目代码仓库位于 [https://github.com/kinegratii/borax/](https://github.com/kinegratii/borax/) 。同时使用 Gitee 作为国内镜像，位于 [https://gitee.com/kinegratii/borax](https://gitee.com/kinegratii/borax) 。

## 话题(Topics)

- **Borax.Calendar**:  [农历](guides/lunardate) | [节日(festivals2)](guides/festivals2)  | [日期节日序列化](guides/festivals2-serialize) | [生日](guides/birthday) | [工具类](guides/calendars-utils)
- **Borax.Datasets**: [数据连接(Join)](guides/join) | [列选择器(fetch)](guides/fetch) 
- **Borax.DataStructures**:  [树形结构](guides/tree) | [cjson](guides/cjson) 
- **Borax.Numbers:**: [中文数字](guides/numbers) |  [百分数](guides/percentage)
- **Borax.Pattern**: [单例模式](guides/singleton) | [选项Choices](guides/choices)
- **其他**: [序列号生成器(Pool)](guides/serial_pool) | [Tkinter界面](guides/ui)
- **已废弃**: [节日](guides/festival)

## 文章(Posts)

-  [农历与节日](guides/festivals2-usage) 

## 开发(Development)

- **代码仓库**：[Github](https://github.com/kinegratii/borax/) | [Gitee (镜像)](https://gitee.com/kinegratii/borax)
- **项目开发**:  [版本日志](changelog) | [技术文档(外链)](http://fd8cc08f.wiz06.com/wapp/pages/view/share/s/3Zzc2f0LJQ3w2TWIQb0ZMSna1zg4gs1vPQmb2vlh9M2zhqK8)
- **发布日志**: [v3.5](release-note/v350) | [v3.5.6](release-note/v356)

## 快速开始(Quickstart)


### 安装

Borax 要求 Python3.5+ ,可以通过 *pip* 安装 ：

```shell
$ pip install borax
```

### 导入

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

### 函数

borax 库在函数定义和调用方面，尽可能按照 [PEP3102](https://www.python.org/dev/peps/pep-3102/) 声明函数参数，即某些参数必须以关键字形式传入参数。

```
borax.choices.Items(value, display=None, *, order=None)
```

### 类型标注

从 v1.2.0 开始，部分模块支持 [Typing Hint](https://docs.python.org/3/library/typing.html) 。