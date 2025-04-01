# festivals2 模块

> 模块： `borax.calendars.festivals2`

> Updated in 4.1.1: SolarFestival和LunarFestival的freq参数支持字符串形式。
>
> Updated in 4.1.0：新增 Festival.code属性。
>
> Updated in 3.5.6: 星期型节日(WeekFestival)类支持倒数序号。如：“国际麻风节(1月最后一个星期天)”
>
> Updated in 3.5.6: 星期型节日(WeekFestival)类支持每月频率。
>
> Add in 3.5.0


## 概述

`borax.calendars.festivals2` 模块是实现常见节日的节日库，你可以使用它进行节日的计算和推导。

### 常量定义

`festival2` 定义了一些常量，这些常量通常归属于一个类，并使用大写字母的变量命名形式。本文档仅列出那些属于 public 权限的常量类。

#### FreqConst

FreqConst 表示节日的频率，用于设置 `Festival` 的 `freq` 参数。

| 定义                  | 描述     |
| --------------------- | -------- |
| FreqConst.YEARLY = 0  | 表示每年 |
| FreqConst.MONTHLY = 1 | 表示每月 |

#### FestivalCatalog

FestivalCatalog 定义了一些节日的分类标签，可以通过 `Festival.catalog` 属性进行读写。

默认支持以下标签。

```python
class FestivalCatalog:
    basic = 'basic'
    event = 'event'
    life = 'life'
    public = 'public'
    tradition = 'tradition'
    term = 'term'
    other = 'other'
    
    CATALOGS = ['basic', 'term', 'public', 'tradition', 'event', 'life', 'other']
```

节日标签用于同一日期有多个节日时，这些节日之间的先后排序问题。

```python
amy_birthday = SolarFestival(month=10,day=1, catalog='event')
```

如上例子，`amy_birthday` 总是在国庆节（其标签为 basic）之后。

## 基础数据结构 - WrappedDate


### 定义

`WrappedDate` 是公历日期和农历日期的包裹类。属性定义如下：

| 属性:类型       | 描述       |
| --------------- | ---------- |
| solar:date      | 公历日期   |
| lunar:LunarDate | 农历日期   |
| name:str        | 名称、标签 |


为了赋值方便，`WrappedDate` 支持 `__iter__`，可以直接使用类似 `sd, ld = wd` 的方式赋值。

使用示例

```python
from datetime import date
from borax.calendars.festivals2 import WrappedDate
 
wd = WrappedDate(date(2021, 1, 1), name='Demo')
# 以下两句也可以简化为  sd, ld = wd
sd = wd.solar
ld = wd.lunar
print(sd) # 2021-01-01
print(ld) # LunarDate(2020, 11, 18, 0)
```
### 日期计算

`WrappedDate` 也支持日期的计算。原则是 **只要操作数中有一个是WrappedDate对象，结果就是WrappedDate对象**。

| 左操作数         | 操作符 | 右操作数         | 结果        |
| ---------------- | ------ | ---------------- | ----------- |
| WrappedDate      | +      | timedelta        | WrappedDate |
| timedelta        | +      | WrappedDate      | WrappedDate |
| date / LunarDate | -      | WrappedDate      | timedelta   |
| WrappedDate      | -      | date / LunarDate | timedelta   |
| WappedDate       | -      | timedelta        | WappedDate  |


### 序列化

 `WrappedDate` 支持编码序列化，参见 日期序列化 一节。


## 基础数据结构 - Period

Period 是一个工具类，提供了一系列方法，这些方法均返回一个包含起始日期和终止日期的二元素元组。

| 方法                                                         | 描述              |
| ------------------------------------------------------------ | ----------------- |
| Period.solar_year(year) -> Tuple[date, date]                 | 公历year年        |
| Period.solar_month(year, month) -> Tuple[date, date]         | 公历year年month月 |
| Period.lunar_year(year) -> Tuple[LunarDate, LunarDate]       | 农历year年        |
| Period.lunar_month(year, month, leap=_IGNORE_LEAP_MONTH) -> Tuple[LunarDate, LunarDate] | 农历year年month月 |


需要注意的是，当leap为默认值且农历year年month月有闰月时，将返回的是两个月时间段的起始日期。下面是 `lunar_month` 方法不同取值的返回的结果。


| (日期范围)                     | 无闰月（year=2020,month=5） | 有闰月（year=2020,month=4） |
| ------------------------------ | --------------------------- | --------------------------- |
| leap=_IGNORE_LEAP_MONTH (默认) | 五月初一  ~ 五月三十        | 四月初一 ~ 闰四月廿九       |
| leap=0                         | 五月初一  ~ 五月三十        | 四月初一 ~ 四月三十         |
| leap=1                         | 五月初一  ~ 五月三十        | 闰四月初一 ~ 闰四月廿九     |


## 节日定义

节日是对日期（公历和农历）的进一步抽象，Borax支持下列几种形式的节日。

| 节日                          | 表示法                                                     | 规范化描述                |
| ----------------------------- | ---------------------------------------------------------- | ------------------------- |
| 元旦                          | SolarFestival(month=1, day=1)                              | 农历每年正月初一          |
| 中秋节                        | LunarFestival(month=8, day=15)                             | 农历每年八月十五          |
| 母亲节（每年5月第二个周日）   | WeekFestival(month=5, index=2, week=calendar.SUNDAY)       | 公历每年5月第2个星期日    |
| 除夕                          | LunarFestival(day=-1)                                      | 农历每年最后一天          |
| 程序员节                      | SolarFestival(freq=FreqConst.YEARLY，day=256)              | 公历每年第256天           |
| 清明节                        | TemFestival(name="清明")                                   | 公历每年清明              |
|                               | TermFestival(name='qm')                                    | 公历每年清明 <sup>1</sup> |
|                               | TermFestival('清明')                                       | 公历每年清明 <sup>2</sup> |
| 入梅 <sup>3</sup>             | TermFestival(term='芒种', nth=1, day_gz='丙', name='入梅') | 公历每年芒种之后第1个丙日 |
| 每月5日                       | SolarFestival(freq=FreqConst.MONTHLY， day=5)              | 公历每月5日               |
| 国际麻风节 <sup>4</sup>       | WeekFestival(month=1, index=-1, week=calendar.SUNDAY)      | 公历1月倒数第1个星期日    |
| 每月最后一个周日 <sup>5</sup> | WeekFestival(month=0, index=-1, week=calendar.SUNDAY)      | 公历每月倒数第1个星期日   |



1. (v3.5.6新增)。参见 `TermFestival`。
2. (v3.5.6新增)。参见 `TermFestival`。
2. (v3.5.6新增)。参见 `TermFestival`。
2. (v3.5.6新增)。参见 `WeekFestival` 。
2. (v3.5.6新增)。参见 `WeekFestival` 。

festivals模块使用4个类表示节日。

### SolarFestival

```python
class SolarFestival(*, day: int, freq: int = FreqConst.YEARLY, month: int = 0, name: str = None)
```

参数定义

| 参数  | 描述                                                         | 取值                                           |
| ----- | ------------------------------------------------------------ | ---------------------------------------------- |
| freq  | 节日频率，“每年”或“每月”，默认“每年”。                       | 0/yearly/y:每年；1/monthly/m:每月 <sup>1</sup> |
| month | 月份。                                                       | 0,1-12                                         |
| day   | 日期序号。当month取值0时，表示一年的第几天；否则表示该月的第几天。允许取负值，表示一年/一个月的倒数 第几天。 |                                                |

1. v4.1.1 新增字符串形式。

6种形式定义

| 定义 | 描述 |
| ---- | ---- |
| SolarFestival(month=1, day=1) | '公历每年1月1日' |
| SolarFestival(month=1, day=-1) | '公历每年1月最后1天' |
| SolarFestival(day=1) | '公历每年第1天' |
| SolarFestival(day=-1) | '公历每年最后1天' |
| SolarFestival(freq=FreqConst.MONTHLY, day=1) | '公历每月1日' |
| SolarFestival(freq=FreqConst.MONTHLY, day=-1) | '公历每月最后1天' |

### LunarFestival

```python
class LunarFestival(*, day:int, freq:int=FreqConst.YEARLY, month:int=0, leap:int=_IGNORE_LEAP_MONTH, name: str=None)
```

参数定义

| 参数  | 描述                                                         | 取值                                           |
| ----- | ------------------------------------------------------------ | ---------------------------------------------- |
| freq  | 节日频率，“每年”或“每月”，默认“每年”。                       | 0/yearly/y:每年；1/monthly/m:每月 <sup>1</sup> |
| month | 月份。                                                       | 0,1-12                                         |
| leap  | 闰月标记。取值参见 `LeapConst`。                             | LeapConst.MIXED                                |
| day   | 日期序号。当month未设置时，表示一年的第几天；否则表示该月的第几天。允许取负值，表示一年/一个月的倒数 第几天。 |                                                |

1. v4.1.1 新增字符串形式。

### WeekFestival

> Updated in 3.5.6: index参数支持负数，表示倒数计数。month支持取值0，表示每月性节日。

```python
class WeekFestival(*, month: int, index: int, week: int, name: str = None)
```

参数定义

| 参数  | 描述                                 | 取值      |
| ----- | ------------------------------------ | --------- |
| month | 月份。取值为 0 ~ 12                  | 0,1-12    |
| index | 序号。支持正向计数和倒数计数。       | 1-9,-1--9 |
| week  | 星期表示。同`calendar.MONTHDAY` 等。 | 0-6       |

### TermFestival

> Updated in 3.5.6: 新增term参数，原有的index参数被废弃。term和name参数支持拼音首字符形式。

v3.5.6以上。

```python
class TermFestival(term: Union[int, str] = None, nth: int = 0, day_gz: str = None, **kwargs
```

v3.5.1-v3.5.5

```python
class TermFestival(*，index:int=None, name:str=None)
```

支持以下几种方式定义，（以小寒为例子）。

```python
TermFestival(0) # 仅3.5.6+
TermFestival('小寒') # 仅3.5.6+
TermFestival('xh') # 仅3.5.6+
TermFestival('XH') # 仅3.5.6+

TermFestival(name='小寒')
TermFestival(index=0)
```

参数定义

| 参数   | 描述                                       | 备注      |
| ------ | ------------------------------------------ | --------- |
| term   | 节气，取值节气序号、中文名称、拼音首字母。 | 3.5.6新增 |
| index  | 节气序号。                                 |           |
| name   | 节气名称。                                 |           |
| nth    | 计数，可取值负数，表示倒数计数。           |           |
| day_gz | 天干或地支标签。                           |           |

## Festival属性

### code

> Add in 4.1.0

类型：str，编码字符串。 `FestivalLibrary` 以此属性作为唯一性的标志。

需要注意的是该属性使用 `cached_property` 进行修饰。

### name

类型：str，节日名称，如“元旦”、“中秋节”等。

### description

> Add in 3.5.1

类型：str，节日的标准化描述，如“公历每年1月1日”、“公历每年八月十五”、“公历每年6月第2个星期六”等。

例子

```python
import calendar
from borax.calendars.festivals2 import SolarFestival, LunarFestival, WeekFestival

print(SolarFestival(month=1, day=1).description) # '公历每年1月1日'
print(SolarFestival(month=1, day=-1).description) # '公历每年1月最后1天'
print(SolarFestival(day=1).description) # '公历每年第1天'
print(LunarFestival(month=1, day=1).description) # '农历每年正月初一'
print(WeekFestival(month=5, index=2, week=calendar.SUNDAY, name='母亲节').description) # '公历5月第2个星期日'
```

### catalog

> Add in 3.5.6

类型:str，节日的分类标识。

## Festival API

### set_name

方法签名

```python
Festival.set_name(name:str)
```

设置节日对象的 name。

### gets

> Add in v3.5.1

方法签名

```
Festival.gets(*args)
```

获取一个或多个属性的值。

### at

方法签名

```python
Festival.at(year:int, month:int=0, leap:int=0) -> MixdDate
```

返回在给定年、年月的时间段的一个日期。

- 在 `LunarFestival` 参数表示农历年月日，返回一个 `LunarDate` 对象
-  其余三个类的参数表示公历年月日，此时 leap 参数无意义，返回一个 `datetime.date` 对象
- 当未找到或者找到一个以上的，抛出 `FestivalError` 异常

### is_


```python
Festival.is_(date_obj:MixedDate) -> bool
```

判断给定的日期是否是该节日，返回布尔值。

### iter_days

```python
Festival.iter_days(start_date:Option[MixedDate]=None, end_date:Option[MixedDate]=None, reverse=False) -> Iterable[None, None, MixedDate]
```

返回在 start_date 和 end_date 之间（含起止日期）匹配本 Festival 的日期列表的迭代器。

- 日期期间的最大范围为 [LunarDate.min, LunarDate.max]
- 返回的是一个迭代器，而不是包含具体日期对象的列表
- reverse=False，时间正序；reverse=False，时间倒序。

例如，获取未来每年除夕节日的公历和公历日期：

```python
from datetime import date
from borax.calendars.festivals2 import LunarFestival,Period
chuxi = LunarFestival(month=12, day=-1)
for wd in chuxi.list_days(start_date=date.today()):
    sd, ld = wd
    print("%s %s".format(sd.strftime("%y-%m-%d"), ld.cn_str()))
```

### list_days

```python
Festival.list_days(start_date=None, end_date=None, reverse=False, count=-1) -> List[WrappedDate]
```

返回在 start_date 和 end_date 之间（含起止日期）匹配本 Festival 的日期列表。

- start_date, end_date, reverse 的参数意义同 iter_days 方法
- 返回一个日期列表。
- count表示日期列表的长度。

### list_days_in_future

> Add in v3.5.5

```python
Festival.list_days_in_future(end_date=None, reverse: bool = False, count: int = -1) -> List[WrappedDate]
```

返回今后时间（[today, end_date]）之间（含起止日期）匹配本 Festival 的日期列表。

### list_days_in_past

> Add in v3.5.5

```python
Festival.list_days_in_past(end_date=None, reverse: bool = False, count: int = -1) -> List[WrappedDate]
```

返回过去时间（[today, end_date]）之间（含起止日期）匹配本 Festival 的日期列表。

### get_one_day

```python
Festival.get_one_day(start_date=None, end_date=None) -> Optional[WrappedDate]
```

返回在 start_date 和 end_date 之间（含起止日期）匹配本 Festival 的第一个日期。

- start_date, end_date 的参数意义同 iter_days 方法
- 返回一个日期，类型为 WrappedDate。

### 倒计时

```python
Festival.countdown(date_obj: MixedDate = None) -> Tuple[int, Optional[WrappedDate]]
```

计算本 festival 匹配的日期距离 date_obj 的天数及其日期。

```python
from borax.calendars.festivals2 import LunarFestival
 
spring_festival = LunarFestival(month=1, day=1)
print(spring_festival.countdown()) # (273, <WrappedDate:2022-02-01(二〇二二年正月初一)>)
```

