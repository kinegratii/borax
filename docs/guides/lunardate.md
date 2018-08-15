# lunardate 模块

> 模块： `borax.calendars.lunardate`

## 概述

`lunardate` 模块是一个处理中国农历日期的工具库，使用 GPLv3 开源协议发布。主要功能有：

- 支持1900 - 2100 （农历）年的日期表示
- 支持干支纪年、节气等
- 使用 Typing Hints

具体的起止日期如下表：

| 项目 | 起始日 | ... | 截止日 |
| ------ | ------ | ------ | ------ |
| 公历 | 1990年1月31日 | ... | 2101年1月8日 |
| 农历 | 1900年正月初一日 | ... | 2100年十二月二十九日 |
| offset | 0 | ... | 73391 |

本模块的代码是基于 [python-lunardate](https://github.com/lidaobing/python-lunardate) 和 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 修改和重写。

## 创建日期对象

可以通过以下几种方法创建。

**▶ 农历日期**

根据农历年、月、日、闰月标志等4个参数创建一个新对象，这也是完全确定一个农历日期的主键参数。

```
>>>from borax.calendars.lunardate import LunarDate
>>>LunarDate(2018, 7, 1)
LunarDate(2018, 7, 1, 0)
```

**▶ 公历日期**

将公历日期转化为农历日期。

```
>>>ld = LunarDate.from_solar_date(2018, 8, 11)
>>>ld
LunarDate(2018, 7, 1, 0)
```

**▶ 特定的日期**

获取今日的农历日期。

```shell
>>>ld = LunarDate.today()
>>>ld
LunarDate(2018, 7, 1, 0)
```

日期范围的上下限

```shell
>>>LunarDate.min
LunarDate(1990, 1, 1, 0)
>>>LunarDate.max
LunarDate(2100, 12, 29, 0)
```

## 属性

和公历日期对象 `datetime.date` 类似，`LunarDate` 是不可变对象(Immutable Object)，可以作为字典的键值。

可用的属性如下（以 `LunarDate(2018, 6, 26, False)` 为例）：

| 属性 | 类型 | 描述 | 示例值 |
| ------ | ------ | ------ | ------ |
| year | `int` | 农历年 | 2018 |
| month | `int` | 农历月 | 6 |
| day | `int` | 农历日 | 26 |
| leap | `bool` | 是否闰月 | False |
| term | `str` 或 `None` | 节气名称 | 立秋 |
| cn_year | `str` | 中文年 | 二〇一八年 |
| cn_month | `str` | 中文月 | 六月 |
| cn_day | `str` | 中文日 | 廿六日 |
| gz_year | `str` | 干支年份 | 戊戌 |
| gz_month | `str` | 干支月份 | 庚申 |
| gz_day | `str` | 干支日 | 辛未 |


## 显示方法

一共有三种显示方式：

- 默认表示法(`__str__`)
- 汉字表示法(`cn_str`)，为了统一字符串长度，日期使用 “廿六” 形式，而不是 “二十六”
- 干支表示法(`gz_str`)

例子：

```shell
>>>ld = LunarDate(2018, 6, 26, False)
>>>ld.cn_str()
'2018年六月廿六日'
>>>ld.gz_str()
'戊戌年庚申月辛未日'
```

## 公历转化

- **LunarDate.to_solar_date()**

将当前日期转化为公历日期

```
>>> ld = LunarDate(2018, 6, 26, False)
>>>ld.to_solar_date()
datetime.date(2018, 8, 7)
```

## 日期推算

**▶ 加减操作符**


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

**▶ 日期推算**

**before/after函数**

返回向前/向后推算 n 天的日期。

```
>>> ld = LunarDate(2018, 6, 3)
>>>ld.after(3)
LunarDate(2018, 6, 6)
>>>ld.before(2)
LunarDate(2018, 6, 1)
```


## 日期比较

两个 `LunarDate` 对象可以进行比较，比如表达式 `LunarDate(2018, 6, 2) > LunarDate(2018, 6, 14)` 的值为 True 。

 `LunarDate` 和 `datetime.date` 的对象无法进行比较，会抛出 `TypeError` 异常。


