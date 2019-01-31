# Borax


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
[![PyPI - Status](https://img.shields.io/pypi/status/borax.svg)](https://github.com/kinegratii/borax)
[![Build Status](https://travis-ci.org/kinegratii/borax.svg?branch=master)](https://travis-ci.org/kinegratii/borax)



## 概述

Borax 是一个的 Python3 开发工具集合库,涉及到：

 - 设计模式
 - 数据结构及其实现
 - 一些简单函数的封装

## 安装

Borax 要求 Python 的版本至少为 3.5 以上。使用 *pip* ：

```shell
$ pip install borax
```

## 使用示例

### 农历模块

> 本模块的数据和算法引用自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 。

获取今天的农历日期，日期推算

```
>>>from borax.calendars.lunardate import LunarDate
>>>LunarDate.today()
LunarDate(2018, 7, 1, 0)
>>>ld = LunarDate.from_solar_date(2018, 8, 11)
>>>ld
LunarDate(2018, 7, 1, 0)
>>>ld.after(10)
LunarDate(2018, 7, 11, 0)
```

### Choices 模块

在 django models 中使用 `choices` 。

```python
from django.db import models
from borax import choices

class GenderChoices(choices.ConstChoices):
    MALE = choices.Item(1, 'male')
    FEMALE = choices.Item(2, 'female')
    UNKOWN = choices.Item(3, 'unkown')
    
class Student(models.Model):        
    gender = models.IntergerFIeld(
        choices=GenderChoices,
        default=GenderChoices.UNKOWN
    )
```

### Fetch

从数据序列中选择一个或多个字段的数据。

```python
from borax.fetch import fetch

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

## 文档

在线文档托管在 [https://kinegratii.github.io/borax](https://kinegratii.github.io/borax) ，由 [docsify](https://docsify.js.org/) 构建。

## 开发特性和规范

- [x] [Typing Hints](https://www.python.org/dev/peps/pep-0484/)
- [x] [Flake8 Code Style](http://flake8.pycqa.org/en/latest/)
- [x] [nose](https://pypi.org/project/nose/)
- [x] [Travis CI](https://travis-ci.org)
- [x] [Docsify](https://docsify.js.org)

## 开源协议

MIT License (MIT)