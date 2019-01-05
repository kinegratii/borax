# lunardate 模块

> 模块： `borax.calendars.lunardate`

## 概述

`lunardate` 模块是一个处理中国农历日期的工具库。支持1900 - 2100 （农历）年范围的日期、干支纪、节气等历法信息。


本模块的数据和算法引用自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) ，具体内容包括：

- 1900-2100年农历月份信息
- 节气数据及其表示方法
- 干支纪年算法

项目代码是基于 [python-lunardate](https://github.com/lidaobing/python-lunardate) 修改和完善，使用 GPLv3 开源协议发布。

## 日期范围

`LunarDate` 实例表示一个具体日期，该类可以表示的日期起止范围如下表：

| 项目 | 起始日 | ... | 2100年 | 2101年 | ... | 截止日 |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 公历 | 1990年1月31日 | ... | 2100年12月31日 | 2101年1月1日 | ... | 2101年1月28日 |
| 农历 | 1900年正月初一日 | ... | 2100年十二月初一日 | 2100年十二月初二日 | ... | 2100年十二月二十九日 |
| offset | 0 | ... | 73383 | 73384 | ... | 73411 |
| 干支 | 庚午年丙子月壬辰日 | ... | 庚申年戊子月丁未日 | - | ... | - |

## 创建日期对象

可以通过以下几种方法创建。

**▶ 农历日期**

依次传入农历年、月、日、闰月标志等4个参数创建一个新对象，其中闰月标志可省略，表示为平月。

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

获取今日/昨日/明日的农历日期。

```shell
>>>LunarDate.today()
LunarDate(2018, 7, 1, 0)
>>>LunarDate.yesterday()
LunarDate(2018, 6, 29, 0)
>>>LunarDate.tomorrow()
LunarDate(2018, 7, 2, 0)
```

`lunardate` 模块可用的日期上下限

```shell
>>>LunarDate.min
LunarDate(1990, 1, 1, 0)
>>>LunarDate.max
LunarDate(2100, 12, 29, 0)
```

## 属性

和公历日期对象 `datetime.date` 类似，`LunarDate` 是不可变对象(Immutable Object)，可以作为字典的键值。

可用的属性如下（以 `LunarDate(2018, 6, 26, False)` 为例）：

| 属性 | 类型 | 描述 | 示例值 | 格式描述符 |
| ------ | ------ | ------ | ------ | ------ |
| year | `int` | 农历年 | 2018 | %y |
| month | `int` | 农历月 | 6 | %m |
| day | `int` | 农历日 | 26 | %d |
| leap | `bool` | 是否闰月 | False | %l |
| term | `str` 或 `None` | 节气名称 | 立秋 | %t |
| cn_year | `str` | 中文年 | 二〇一八年 | %Y |
| cn_month | `str` | 中文月 | 六月 | %M |
| cn_day | `str` | 中文日 | 廿六日 | %D |
| gz_year | `str` | 干支年份 | 戊戌 | %o |
| gz_month | `str` | 干支月份 | 庚申 | %p |
| gz_day | `str` | 干支日 | 辛未 | %q |
| animal | `str` | 年生肖 | 狗 | %a |


## 格式化显示

### 内置方法

一共有三种显示方式：

| 显示方式 | 调用形式 | 示例 | 格式描述符 |
| ------ | ------ | ------ | ------ |
| 默认表示法 | `str(ld)` | LunarDate(2018, 6, 26, False) | - |
| 汉字表示法 | `ld.cn_str()` | 2018年六月廿六日 | %C |
| 干支表示法 | `ld.gz_str()` | 戊戌年庚申月辛未日 | %G |

在汉字表示法中，为了统一字符串长度，日期使用 “廿六” 形式，而不是 “二十六”；“十一月”、“十二月”使用“冬月”、“腊月”形式。

### 自定义

> v1.2.0 新增。

`LunarDate.strftime` 提供了通过格式描述符来自定义显示日期字符串。在“属性”一节中已经列出所有属性的格式描述符。

- 描述符长度为2，由"%"紧跟一个字母组成
- '%l' 将闰月标志格式化为数字，如“0”、“1”
- '%Y'、'%M'、'%D' 三个中文名称不包含“年”、“月”、“日”后缀汉字

例子：

```
>>>today = LunarDate.today()
>>>today.strftime（'%Y-%M-%D')
'二〇一八-六-廿六'
>>>today.strftime('今天的干支表示法为：%G')
'今天的干支表示法为：戊戌年庚申月辛未日'
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


`LunarDate` 支持和 `datetime.timedelta` 或 `datetime.date` 进行加减计算。


| 左操作数类型 | 操作符 | 右操作数类型 | 结果类型 |
| ------ | ------ | ------ | ------ |
| `LunarDate` | + | `datetime.timedelta` | `LunarDate` |
| `datetime.timedelta` | + | `LunarDate` | `LunarDate` |
| `LunarDate` | - | `datetime.timedelta` | `LunarDate` |
| `datetime.date` | - | `LunarDate` | `datetime.timedelta` |
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

返回向前/向后推算 n 天的日期。n 允许取负值，即 `ld.after(5)` 和 `ld.before(-5)` 返回表示同一个日期的实例。

```
>>> ld = LunarDate(2018, 6, 3)
>>>ld.after(3)
LunarDate(2018, 6, 6, 0)
>>>ld.before(2)
LunarDate(2018, 6, 1, 0)
>>>ld.after(-2)
LunarDate(2018, 6, 1, 0)
```

**replace函数**

返回一个替换给定值后的日期对象。

函数签名 `replace(self, *, year=None, month=None, day=None, leap=None)` 所有参数必须以关键字形式传入。如果该日期不存在，将抛出 `ValyeError` 异常。

```
>>>ld = LunarDate(2018, 5, 3)
>>>ld.replace(year=2019)
LunarDate(2019, 5, 3, 0)
>>>ld.replace(leap=True)
ValueError: month out of range
```

## 日期比较

`LunarDate` 支持和 `datetime.date` 对象进行比较，对象所代表的日期更新其“数值”更大。

```
>>>LunarDate(2018, 6, 2) > LunarDate(2018, 6, 14)
False
>>>LunarDate(2018, 6, 2) > date(2018, 6, 2)
True
```
