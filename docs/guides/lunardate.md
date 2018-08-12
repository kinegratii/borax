# lunardate 模块

> 模块： `borax.calendars.lunardate`

## 概述

`borax.calendars.lunardate` 模块是一个处理中国农历日期的工具库，使用 GPLv3 开源协议发布。

主要功能：

- 支持1900 - 2100 （农历）年的日期表示
- 支持日期干支、节气等
- 支持 Typing Hints

`borax.calendars.lunardate.LunarDate` 能够处理 1900 - 2100 年之间的农历日期，具体的起止日期如下表：

| 项目 | 起始日 | ... | 截止日 |
| ------ | ------ | ------ | ------ |
| 公历 | 1990年1月31日 | ... | 2101年1月8日 |
| 农历 | 1900年正月初一日 | ... | 2100年十二月二十九日 |
| offset | 0 | ... | 73391 |

本模块的代码是基于 [python-lunardate](https://github.com/lidaobing/python-lunardate) 和 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 修改和重写。

## 创建日期对象

可以通过以下几种方法创建。

第一，基于农历年月日创建一个新对象。

```
>>>from borax.calendars.lunardate import LunarDate
>>>LunarDate(2018, 7, 1)
LunarDate(2018, 7, 1, 0)
```

第二，获取今日的农历日期。

```
>>>ld = LunarDate.today()
>>>ld
LunarDate(2018, 7, 1, 0)
```
第三，将公历日期转化为农历日期。

```
>>>ld = LunarDate.from_solar_date(2018, 8, 11)
>>>ld
LunarDate(2018, 7, 1, 0)
```

## 属性与方法

`LunarDate` 农历日期对象和公历日期对象 `datetime.date` 类似。

```python
class LunarDate(year:int, month:int, day:int, leap:bool)
```

各个参数的意义如下：

- year ：整数，农历年份，范围为 1900 - 2100 。
- month ： 整数，农历月份，范围为 1 -12 。
- day ： 整数，农历日期，范围为 1 - 29/30 ，具体根据是否为大月决定 。
- leap ： 布尔值，是否为农历闰月。

LunarDate 为不可变对象(Immutable Object)，可以作为字典的键值。


## 公历转化

- **classmethod LunarDate.from_solar_date(year, month, day)**


从公历日期转化为农历日期。

```python
dt2 = LunarDate.from_solar_date(2033, 10, 23)
print(dt2.year)
```

- **LunarDate.to_solar_date()**

将当前日期转化为公历日期

## 日期加减



`LunarDate` 支持和 `datetime.timedelta` 进行加减计算。


| 左操作数类型 | 操作符 | 右操作数类型 | 结果类型 |
| ------ | ------ | ------ | ------ |
| `LunarDate` | + | `datetime.timedelta` | `LunarDate` |
| `datetime.timedelta` | + | `LunarDate` | `LunarDate` |
| `LunarDate` | - | `datetime.timedelta` | `LunarDate` |
| `LunarDate` | - | `datetime.date` | `datetime.timedelta` |
| `LunarDate` | - | `LunarDate` | `datetime.timedelta` |

例子：

```
>>> LunarDate(2018, 6, 3) + timedelta(days=3)
LunarDate(2018, 6, 6, 0)
>>> LunarDate(2018, 6, 18) - LunarDate(2018, 6, 3)
timedelta(days=15)
```

## 日期比较

两个 `LunarDate` 对象可以进行比较，比如表达式 `LunarDate(2018, 6, 2) > LunarDate(2018, 6, 14)` 的值为 True 。

 `LunarDate` 和 `datetime.date` 的对象无法进行比较，会抛出 `TypeError` 异常。


