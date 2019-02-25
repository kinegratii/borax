# lunardate 模块

> 模块： `borax.calendars.lunardate`  协议：GPLv3

## 概述

`lunardate` 模块是一个处理中国农历日期的工具库。支持1900 - 2100 农历年范围的日期、干支纪年、节气等历法信息。


本模块的数据和算法引用自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) ，具体内容包括：

- 1900-2100年农历月份信息
- 干支纪年算法

关于本模块的更多资料可参考文章 [《Borax-Lunar开发笔记》](https://kinegratii.github.io/2019/01/05/lunardate-module/)。

## 常量定义

`lunardate` 提供了下列的模块级常量。 

- **lunardate.MIN_LUNAR_YEAR**

农历可表示的最大年份，值为 2100 。

- **lunardate.MAX_LUNAR_YEAR**

农历可表示的最小年份，值为 1900 。

- **lunardate.MIN_SOLAR_DATE**

农历可表示的日期下限，值为 `datetime.date(1900, 1, 31)`，日期同 `LunarDate.min`。

- **lunardate.MAX_SOLAR_DATE**

农历可表示的日期下限，值为 `datetime.date(2101, 1, 28)`，日期同 `LunarDate.max`。

- **lunardate.MAX_OFFSET**

农历日期的最大偏移量，值为73411。

## 日期范围

`LunarDate` 实例表示一个具体日期，该类可以表示的日期起止范围如下表：

| 项目 | 起始日 | ... | 2100年 | 2101年 | ... | 截止日 |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| 公历 | 1990年1月31日 | ... | 2100年12月31日 | 2101年1月1日 | ... | 2101年1月28日 |
| 农历 | 1900年正月初一 | ... | 2100年腊月初一 | 2100年腊月初二 | ... | 2100年腊月廿九 |
| offset | 0 | ... | 73383 | 73384 | ... | 73411 |
| 干支 | 庚午年丙子月壬辰日 | ... | 庚申年戊子月丁未日 | 庚申年戊子月戊申日 | ... | 庚申年己丑月乙亥日 |

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

和公历日期对象 `datetime.date` 类似，`LunarDate` 是不可变对象(Immutable Object)，可以作为字典的键值。全部属性如下表（以 `LunarDate(2018, 6, 26, False)` 为例）：

| 属性 | 类型 | 描述 | 示例值 | 格式描述符 | 备注 |
| ------ | ------ | ------ | ------ | ------ | ------ |
| year | `int` | 农历年 | 2018 | %y | |
| month | `int` | 农历月 | 6 | %m | |
| day | `int` | 农历日 | 26 | %d | |
| leap | `bool` | 是否闰月 | False | %l | (1) |
| offset | `int` | 距下限的偏移量 | 43287 | - | |
| term | `str` 或 `None` | 节气名称 | 立秋 | %t | |
| cn_year | `str` | 中文年 | 二〇一八年 | %Y | (2) |
| cn_month | `str` | 中文月 | 六月 | %M | (2) |
| cn_day | `str` | 中文日 | 廿六 | %D | (2) |
| gz_year | `str` | 干支年份 | 戊戌 | %o | |
| gz_month | `str` | 干支月份 | 庚申 | %p | |
| gz_day | `str` | 干支日 | 辛未 | %q | |
| animal | `str` | 年生肖 | 狗 | %a | |
| - | `str` | 两位数字的月份 | 06 | %A | |
| - | `str` | 两位数字的日期 | 26 | %B | |

## 格式化显示

### 内置方法

一共有三种显示方式：

| 显示方式 | 调用形式 | 示例 | 格式描述符 |
| ------ | ------ | ------ | ------ |
| 默认表示法 | `str(ld)` | LunarDate(2018, 6, 26, False) | - |
| 汉字表示法 | `ld.cn_str()` | 2018年六月廿六 | %C |
| 干支表示法 | `ld.gz_str()` | 戊戌年庚申月辛未日 | %G |

在汉字表示法中，为了统一字符串长度，日期使用 “廿六” 形式，而不是 “二十六”；“十一月”、“十二月”使用“冬月”、“腊月”形式。

### 格式符描述

> v1.2.0 新增。


- **LunarDate.strftime(fmt)** 

`strftime`通过描述符(Directive)格式化给定的日期字符串。在“属性”一节中已经列出所有属性的格式描述符。

备注信息：

- (1) '%l' 将闰月标志格式化为数字，如“0”、“1”
- (2) '%Y'、'%M'、'%D' 三个中文名称不包含“年”、“月”、“日”后缀汉字

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

`replace(self, *, year=None, month=None, day=None, leap=None)`

返回一个替换给定值后的日期对象。所有参数必须以关键字形式传入。如果该日期不存在，将抛出 `ValyeError` 异常。

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

## 序列化

`LunarDate` 对象支持 pickle 序列化。

```python
import pickle
from borax.calendars.lunardate import LunarDate


ld = LunarDate.today()
with open('data.pickle', 'wb') as f:
    pickle.dump(ld, f)

with open('data.pickle', 'rb') as f:
    l2 = pickle.load(f)
    print(l2) # LunarDate(2018, 7, 24, 0)

```

## LCalendars工具接口

`LCalendars` 提供了一系列的工具方法。

- **LCalendars.ndays(year: int, month: Optional[int] = None, leap: Leap = False) -> int**

返回X年或者X年X月的天数；如输入的年月不存在，将抛出 `ValueError` 异常。
例子：

```
>>>from borax.calendars.lunardate import LCalendars
>>>LCalendars.ndays(2018)
354
>>>LCalendars.ndays(2018, 12)
30
>>>LCalendars.ndays(2017, 6, 1)
30
>>>LCalendars.ndays(2200)
ValueError: year out of range [1900, 2100]
>>>LCalendars.ndays(2017, 7, 1)
ValueError: Invalid month for the year 2017
```
- **LCalendars.iter_year_month(year: int) -> Iterator[Tuple[int, int, int]]**

迭代X年的月份信息，元素返回 *(月份, 该月的天数, 闰月标记)* 的元祖。

例子：

```
>>>from borax.calendars.lunardate import LCalendars
>>>list(LCalendars.iter_year_month(2017))
[(1, 29, 0), (2, 30, 0), (3, 29, 0), (4, 30, 0), (5, 29, 0), (6, 29, 0), (6, 30, 1), (7, 29, 0), (8, 30, 0), (9, 29, 0), (10, 30, 0), (11, 30, 0), (12, 30, 0)]
```

- **LCalendars.create_solar_date(year: int, term_index: Optional[int] = None, term_name: Optional[str] = None) -> datetime.date**

根据节气名称或者序号获取对应的公历日期对象(`dateitime.date`)。`term_index` 和 `term_name` 只需传入一个参数，

`term_index` 取值为 0-23 。其中 小寒的序号为0，立春的序号为2，...冬至的序号为23。

```
>>>LCalendars.create_solar_date(2019, term_name='清明')
2019-04-05
```

- **LCalendars.delta(date1:MDate, date2:MDate) -> int**

计算两个日期相隔的天数，即 `(date1 - date2).days`。


## 参考资料

- [香港天文台农历信息](http://www.hko.gov.hk/gts/time/conversion.htm)
- [农历维基词条](https://en.wikipedia.org/wiki/Chinese_calendar)
- [jjonline/calendar.js](https://github.com/jjonline/calendar.js)
- [lidaobing/python-lunardate](https://github.com/lidaobing/python-lunardate)