# Borax - python3工具集合库


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
![Python package](https://github.com/kinegratii/borax/workflows/Python%20package/badge.svg)
![Codecov](https://codecov.io/github/kinegratii/borax/coverage.svg)
![GitHub license](https://img.shields.io/github/license/kinegratii/borax)
![Document](https://img.shields.io/badge/%E6%96%87%E6%A1%A3-docsify%20%7C%20%E8%AF%AD%E9%9B%80-brightgreen)



## 概述 (Overview)

> github  https://github.com/kinegratii/borax
>
> gitee  https://gitee.com/kinegratii/borax



Borax 是一个Python3工具集合库。包括了以下几个话题：

| 话题（Topics）      | 内容                                                  |
| ------------------- | ----------------------------------------------------- |
| Borax.Calendars     | 1900-2100年的中国农历日期库                           |
| Borax.Choices       | 声明式的选项类。适用于Django.models.choices 定义。    |
| Borax.Datasets      | 记录型数据操作库，包括连结（Join）、列选择（fetch）等 |
| Borax.DataStuctures | 树形结构，json数据                                    |
| Borax.Numbers       | 数字库。包括中文数字、百分数等。                      |
| Borax.Patterns      | 设计模式。包括单例模式、代理对象、延迟对象。          |

## 安装 (Installation)

Borax 要求 Python3.6+ 。

可以通过以下两种方式安装 ：

1) 使用 *pip* ：

```shell
$ pip install borax
```

2) 使用 [poetry](https://poetry.eustace.io/) 工具：

```shell
$ poetry add borax
```

## 使用示例 (Usage)

### Borax.LunarDate: 中国农历日期

一个支持1900-2100年的农历日期工具库。

> 本模块的数据和算法参考自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 。

创建日期，日期推算

```python
from datetime import timedelta
from borax.calendars import LunarDate

# 获取今天的农历日期（农历2018年七月初一）
print(LunarDate.today()) # LunarDate(2018, 7, 1, 0)

# 将公历日期转化为农历日期
ld = LunarDate.from_solar_date(2018, 8, 11)
print(ld) # LunarDate(2018, 7, 1, 0)

# 日期推算，返回10天后的农历日期
print(ld.after(10)) # LunarDate(2018, 7, 11, 0)

# 可以直接与 datetime.timedelta 直接相加减
print(ld + timedelta(days=10)) # LunarDate(2018, 7, 11, 0)
```

格式化字符串

```python
today = LunarDate.today()
print(today.strftime('%Y年%L%M月%D')) # '二〇一八年六月廿六'
print(today.strftime('今天的干支表示法为：%G')) # '今天的干支表示法为：戊戌年庚申月辛未日'
```

### Borax.Festival: 国内外节日

分别计算距离 “春节”、“除夕（农历十二月的最后一天）” 还有多少天

```python
from borax.calendars.festivals2 import SolarFestival

festival = SolarFestival(month=1, day=1)
print(festival.countdown()) # (273, <GeneralDate:2022-02-01(二〇二二年正月初一)>)
```

计算节日及其距离今天（2021年5月4日）的天数
```python

from borax.calendars.festivals2 import FestivalLibrary

library = FestivalLibrary.load_builtin()
for nday, gd_list in library.iter_festival_countdown():
    for gd in gd_list:
        print('{:>3d} {} {}'.format(nday, gd.name, gd))
```

输出结果

```
  0 青年节 2021-05-04(二〇二一年三月廿三)
  5 母亲节 2021-05-09(二〇二一年三月廿八)
  8 护士节 2021-05-12(二〇二一年四月初一)
 28 儿童节 2021-06-01(二〇二一年四月廿一)
<...>
336 清明 2022-04-05(二〇二二年三月初五) 
362 劳动节 2022-05-01(二〇二二年四月初一)

```


### Borax.Numbers: 中文数字处理


不同形式的中文数字

```python
from borax.numbers import ChineseNumbers

# 小写、计量
print(ChineseNumbers.to_chinese_number(204)) # '二百零四'
# 小写、编号
print(ChineseNumbers.order_number(204)) # '二百〇四'
# 大写、计量
print(ChineseNumbers.to_chinese_number(204, upper=True)) # '贰佰零肆'
# 大写、编号
print(ChineseNumbers.to_chinese_number(204, upper=True, order=True)) # '贰佰〇肆'
```

财务金额

```python
from borax.numbers import FinanceNumbers

print(FinanceNumbers.to_capital_str(100000000)) # '壹亿元整'
print(FinanceNumbers.to_capital_str(4578442.23)) # '肆佰伍拾柒万捌仟肆佰肆拾贰元贰角叁分'
print(FinanceNumbers.to_capital_str(107000.53)) # '壹拾万柒仟元伍角叁分'

```

### Borax.Datasets: 数据列选择

从数据序列中选择一个或多个字段的数据。

```python
from borax.datasets.fetch import fetch

objects = [
    {'id': 282, 'name': 'Alice', 'age': 30},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56},
]

names = fetch(objects, 'name')
print(names) # ['Alice', 'Bob', 'Charlie']
```

## 文档 (Document)

文档由 [docsify](https://docsify.js.org/) 构建。

| 源 | 网址 |
| ---- | ---- |
| github | [https://kinegratii.github.io/borax](https://kinegratii.github.io/borax) |
| gitee | [https://kinegratii.gitee.io/borax](https://kinegratii.gitee.io/borax) |

## 开发特性和规范 (Development Features)

- [x] [Typing Hints](https://www.python.org/dev/peps/pep-0484/)
- [x] [Flake8 Code Style](http://flake8.pycqa.org/en/latest/)
- [x] [nose2](https://pypi.org/project/nose2/) | [pytest](https://docs.pytest.org/en/latest/)
- [x] [Github Action](https://github.com/kinegratii/borax/actions)
- [x] [Code Coverage](https://codecov.io/)

## 开源协议 (License)

```
The MIT License (MIT)

Copyright (c) 2015-2021 kinegratii

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```

## 捐赠 (Donate)

如果你觉得这个项目帮助到了你，你可以帮作者们买一杯咖啡表示感谢！

![donation-wechat](docs/images/donation-wechat.png)

