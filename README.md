# Borax - python开发工具集合


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
[![PyPI - Status](https://img.shields.io/pypi/status/borax.svg)](https://github.com/kinegratii/borax)
[![Build Status](https://travis-ci.org/kinegratii/borax.svg?branch=master)](https://travis-ci.org/kinegratii/borax)



## 概述 & 安装

Borax 是一个 Python3 开发工具集合库,涉及到：

 - 设计模式
 - 数据结构及其实现
 - 一些简单函数的封装

使用 *pip* ：

```shell
$ pip install borax
```

## 使用示例

### 中国农历日期

一个支持1900-2100年的农历日期工具库。

> 本模块的数据和算法参考自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 。

创建日期，日期推算

```python
from borax.calendars.lunardate import LunarDate

# 获取今天的农历日期（农历2018年七月初一）
print(LunarDate.today()) # LunarDate(2018, 7, 1, 0)

# 将公历日期转化为农历日期
ld = LunarDate.from_solar_date(2018, 8, 11)
print(ld) # LunarDate(2018, 7, 1, 0)

# 日期推算，返回10天后的农历日期

print(ld.after(10)) # LunarDate(2018, 7, 11, 0)
```

格式化字符串

```python
today = LunarDate.today()
print(today.strftime('%Y-%M-%D')) # '二〇一八-六-廿六'
print(today.strftime('今天的干支表示法为：%G')) # '今天的干支表示法为：戊戌年庚申月辛未日'
```

### 国内外节日

分别计算距离 “春节”、生日（十一月初一）、“除夕（农历十二月的最后一天）” 还有多少天

```python
from borax.calendars.festivals import get_festival, LunarSchema, DayLunarSchema

festival = get_festival('春节')
print(festival.countdown()) # 7

ls = LunarSchema(month=11, day=1)
print(ls.countdown()) # 285

dls = DayLunarSchema(month=12, day=1, reverse=1)
print(dls.countdown()) # 344
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
print(names) # ['Alice', 'Bob', 'Charlie']
```

## 文档

在线文档托管在 [https://kinegratii.github.io/borax](https://kinegratii.github.io/borax) ，由 [docsify](https://docsify.js.org/) 构建。

## 开发特性和规范

- [x] [Typing Hints](https://www.python.org/dev/peps/pep-0484/)
- [x] [Flake8 Code Style](http://flake8.pycqa.org/en/latest/)
- [x] [nose2](https://pypi.org/project/nose2/)
- [x] [Travis CI](https://travis-ci.org)
- [x] [Docsify](https://docsify.js.org)

## 开源协议

MIT License (MIT)

## 捐赠

如果你觉得这个项目帮助到了你，你可以帮作者们买一杯咖啡表示感谢！

![donation-wechat](docs/images/donation-wechat.png)

