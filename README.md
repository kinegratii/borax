# Borax - python开发工具集合


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
[![PyPI - Status](https://img.shields.io/pypi/status/borax.svg)](https://github.com/kinegratii/borax)
[![Build Status](https://travis-ci.org/kinegratii/borax.svg?branch=master)](https://travis-ci.org/kinegratii/borax)



## 概述 & 安装

Borax 是一个的 Python3 开发工具集合库,涉及到：

 - 设计模式
 - 数据结构及其实现
 - 一些简单函数的封装

使用 *pip* ：

```shell
$ pip install borax
```

## 使用示例

### 中国农历日期

> 本模块的数据和算法引用自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 。

获取今天的农历日期（农历2018年七月初一）

```
>>>from borax.calendars.lunardate import LunarDate
>>>LunarDate.today()
LunarDate(2018, 7, 1, 0)
```

将公历日期转化为农历日期

```
>>>ld = LunarDate.from_solar_date(2018, 8, 11)
>>>ld
LunarDate(2018, 7, 1, 0)
```

日期推算，返回10天后的农历日期

```
>>>ld.after(10)
LunarDate(2018, 7, 11, 0)
```

### 国内外节日

计算距离“春节”还有多少天

```
>>>from borax.calendars.festivals import get_festival
>>>festival = get_festival('春节')
>>>festival.countdown()
7
```

计算距离生日（十一月初一）还有多少天

```
>>>from borax.calendars.festivals import LunarSchema
>>>ls = LunarSchema(month=11, day=1)
>>>ls.countdown()
285
```

计算距离“除夕（农历十二月的最后一天）”还有多少天
```
>>>from borax.calendars.festivals import DayLunarSchema
>>>dls = DayLunarSchema(month=12, day=1, reverse=1)
>>>dls.countdown()
344
```

### 大写金额

将金额转化为符合标准的大写数字。

```
>>> from borax.finance import financial_amount_capital
>>> financial_amount_capital(100000000)
'壹亿元整'
>>>financial_amount_capital(4578442.23)
'肆佰伍拾柒万捌仟肆佰肆拾贰元贰角叁分'
>>>financial_amount_capital(107000.53)
壹拾万柒仟元伍角叁分
```

### 单例模式

```
>>>from borax.patterns.singleton import MetaSingleton
>>>class SingletonM(metaclass=MetaSingleton):pass
>>>a = SingletonM()
>>>b = SingletonM()
>>>id(a) == id(b)
True
```

### 数据拾取

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