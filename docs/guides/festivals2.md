# festivals2 模块

> 模块： `borax.calendars.festivals2`

> Add in 3.5.0


## 概述

`borax.calendars.festivals2` 模块是实现常见节日的节日库，你可以使用它进行节日的计算和推导。

### 常量定义

`festival2` 定义了一些常量，这些常量通常归属于一个名称以“Const”结尾的类，并使用大写字母的变量命名形式。

#### FreqConst

FreqConst 表示节日的频率，用于设置 `Festival` 的 `freq` 参数。

| 定义                  | 描述     |
| --------------------- | -------- |
| FreqConst.YEARLY = 0  | 表示每年 |
| FreqConst.MONTHLY = 1 | 表示每月 |

#### LeapConst

LeapConst表示农历闰月的标志，用于 `Period` 、`Festival` 对象初始化操作。

| 定义                 | 表示 |
| -------------------- | ---- |
| LeapConst.NORMAL = 0 | 平月 |
| LeapConst.LEAP = 1   | 闰月 |
| LeapConst.MIXED = 2  | 混合 |


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

| 方法                                                     | 描述              |
| -------------------------------------------------------- | ----------------- |
| Period.solar_year(year)                                  | 公历year年        |
| Period.solar_month(year, month)                          | 公历year年month月 |
| Period.lunar_year(year)                                  | 农历year年        |
| Period.lunar_month(year, month, leap=_IGNORE_LEAP_MONTH) | 农历year年month月 |


需要注意的是，当leap为默认值且农历year年month月有闰月时，将返回的是两个月时间段的起始日期。下面是 `lunar_month` 方法不同取值的返回的结果。


| (日期范围)                     | 无闰月（year=2020,month=5） | 有闰月（year=2020,month=4） |
| ------------------------------ | --------------------------- | --------------------------- |
| leap=_IGNORE_LEAP_MONTH (默认) | 五月初一  ~ 五月三十        | 四月初一 ~ 闰四月廿九       |
| leap=0                         | 五月初一  ~ 五月三十        | 四月初一 ~ 四月三十         |
| leap=1                         | 五月初一  ~ 五月三十        | 闰四月初一 ~ 闰四月廿九     |


## 节日定义

节日是对日期（公历和农历）的进一步抽象。

| 节日                        | 表示法                                               | 规范化描述             |
| --------------------------- | ---------------------------------------------------- | ---------------------- |
| 元旦                        | SolarFestival(month=1, day=1)                        | 农历每年正月初一       |
| 中秋节                      | LunarFestival(month=8, day=15)                       | 农历每年八月十五       |
| 母亲节（每年5月第二个周日） | WeekFestival(month=5, index=2, week=calendar.SUNDAY) | 公历每年5月第2个星期日 |
| 除夕                        | LunarFestival(month=12, day=-1)                      | 农历每年腊月最后一天   |
|                             | LunarFestival(day=-1)                                | 农历每年最后一天       |
| 程序员节                    | SolarFestival(freq=FreqConst.YEARLY，day=256)         | 公历每年第256天        |
| 清明节                      | TemFestival(name="清明")                             | 公历每年清明           |
| 每月5日                     | SolarFestival(freq=FreqConst.MONTHLY， day=5)       | 公历每月5日            |

festivals模块使用4个类表示节日，各个类的初始化函数签名如下：


```python
class SolarFestival(day, freq=FreqConst.YEARLY, year=0, month=0)
class WeekFestival(month, index, week)
class TermFestival(name)
class LunarFestival(day, freq=FreqConst.YEARLY, year=0, month=0, leap=0)
```

各参数定义如下：

| 参数  | 描述                                                         | 默认值           |
| ----- | ------------------------------------------------------------ | ---------------- |
| freq  | 节日频率，“每年”或“每月”，默认“每年”。取值参见 `FreqConst`。 | FreqConst.YEARLY |
| year  | 年份。默认不设置                                             |                  |
| month | 月份。取值为 0 ~ 12                                          | 0                |
| leap  | 闰月标记。取值参见 `LeapConst`。                             | LeapConst.MIXED  |
| day   | 日期序号。当month未设置时，表示一年的第几天；否则表示该月的第几天。允许取负值，表示一年/一个月的倒数 第几天。 | 必要参数         |
| index | 序号。从1开始计数。                                          | 必要参数         |
| week  | 星期表示。同`calendar.MONTHDAY` 等。                         | 必要参数         |

## Festival属性

### name

类型：str，节日名称，如“元旦”、“中秋节”等。

### description

> Add in v3.5.1

类型：str，节日的标准化描述，如“公历每年1月1日”、“公历每年八月十五”、“公历每年6月第2个星期六”等。

设置节日对象的 name。

例子

```python
import calendar
from borax.calendars.festivals2 import SolarFestival, LunarFestival, WeekFestival

print(SolarFestival(month=1, day=1).description) # '公历每年1月1日'
print(SolarFestival(month=1, day=-1).description) # '公历每年1月倒数第1天'
print(SolarFestival(day=1).description) # '公历每年第1天'
print(LunarFestival(month=1, day=1).description) # '农历每年正月初一'
print(WeekFestival(month=5, index=2, week=calendar.SUNDAY, name='母亲节').description) # '公历5月第2个星期日'
```



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
- reverse 表示是否反向

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

### get_one_day

```python
Festival.get_one_day(start_date=None, end_date=None) -> Optional[WrappedDate]
```

返回在 start_date 和 end_date 之间（含起止日期）匹配本 Festival 的第一个日期。

- start_date, end_date 的参数意义同 iter_days 方法
- 返回一个日期，类型为 WrappedDate。

### 倒计时

```python
Festival.countdown(date_obj: MixedDate = None) -> Tuple[int, Optional[WrappedDate]])
```

计算本 festival 匹配的日期距离 date_obj 的天数及其日期。

```python
from borax.calendars.festivals2 import LunarFestival
 
spring_festival = LunarFestival(month=1, day=1)
print(spring_festival.countdown()) # (273, <WrappedDate:2022-02-01(二〇二二年正月初一)>)
```

## FestivalLibrary：节日集合库

`FestivalLibrary` 是集合容器类，提供了一些常用的节日。此类继承自 `collections.UserList` ，拥有  append/remove/extend/insert等方法。

```python
class FestivalLibrary(collections.UserList):
    pass
```

### get_code_set

> Add in v3.5.1

```
FestivalLibrary.get_code_set()
```

获取当前所有节日的code集合。

### extend_unique

> Add in v3.5.1

```
FestivalLibrary.extend_unique(other)
```

添加多个节日对象，类似于 extend 方法，但是如果code已经存在则不再加入。

### load_file

```python
FestivalLibrary.load_file(cls, file_path: Union[str, Path]) -> 'FestivalLibrary'
```

从文件 file_path 中加载节日数据。

### load_builtin

```python
FestivalLibrary.load_builtin(cls, identifier: str = 'zh-Hans') -> 'FestivalLibrary'
```

加载Borax提供的节日库数据。

### get_festival

```python
FestivalLibrary.get_festival(self, name: str) -> Optional[Festival]
```

根据名称获取对应的 Festival 对象。

### get_festival_names

```python
FestivalLibrary.get_festival_names(self, date_obj: MixedDate) -> list
```

获取某一个日期的节日名称列表。

### iter_festival_countdown

```python
FestivalLibrary.iter_festival_countdown(self, countdown: Optional[int] = None, date_obj: MixedDate = None) -> Iterator[Tuple[int, List]]
```

迭代获取节日的日期。

```python

from borax.calendars.festivals2 import FestivalLibrary

fl = FestivalLibrary.load_builtin()
for nday, gd_list in fl.iter_festival_countdown():
    for gd in gd_list:
        print('{:>3d} {} {}'.format(nday, gd.name, gd))

```

输出

```
  7 儿童节 2021-06-01(二〇二一年四月廿一)
 20 端午节 2021-06-14(二〇二一年五月初五)
 26 父亲节 2021-06-20(二〇二一年五月十一)
 68 建军节 2021-08-01(二〇二一年六月廿三)
 81 七夕 2021-08-14(二〇二一年七月初七)
 89 中元节 2021-08-22(二〇二一年七月十五)
108 教师节 2021-09-10(二〇二一年八月初四)
119 中秋节 2021-09-21(二〇二一年八月十五)
129 国庆节 2021-10-01(二〇二一年八月廿五)
142 重阳节 2021-10-14(二〇二一年九月初九)
184 感恩节 2021-11-25(二〇二一年十月廿一)
210 冬至 2021-12-21(二〇二一年冬月十八)
213 平安夜 2021-12-24(二〇二一年冬月廿一)
214 圣诞节 2021-12-25(二〇二一年冬月廿二)
221 元旦 2022-01-01(二〇二一年冬月廿九)
230 腊八节 2022-01-10(二〇二一年腊月初八)
251 除夕 2022-01-31(二〇二一年腊月廿九)
252 春节 2022-02-01(二〇二二年正月初一)
265 情人节 2022-02-14(二〇二二年正月十四)
266 元宵节 2022-02-15(二〇二二年正月十五)
287 妇女节 2022-03-08(二〇二二年二月初六)
291 植树节 2022-03-12(二〇二二年二月初十)
311 愚人节 2022-04-01(二〇二二年三月初一)
315 清明 2022-04-05(二〇二二年三月初五)
341 劳动节 2022-05-01(二〇二二年四月初一)
344 青年节 2022-05-04(二〇二二年四月初四)
348 母亲节 2022-05-08(二〇二二年四月初八)
352 护士节 2022-05-12(二〇二二年四月十二)
```

## 序列化和存储


## 综合使用示例

###  两头春、无头春

```python
# 农历两头春，无头春。在农历year年时间段，立春的个数。

from borax.calendars.festivals2 import TermFestival, Period
from borax.calendars.lunardate import MIN_LUNAR_YEAR, MAX_LUNAR_YEAR

tf = TermFestival(name='立春')
for year in range(MIN_LUNAR_YEAR, MAX_LUNAR_YEAR):
    start_date, end_date = Period.lunar_year(year)
    ncount = len(tf.list_days(start_date, end_date))
    print('{}({}) - {}({})    {}'.format(
        start_date.cn_str(),
        start_date.to_solar_date(),
        end_date.cn_str(),
        end_date.to_solar_date(),
        ncount
    ))

```


输出
```
...
 
二〇一一年正月初一(2011-02-03) - 二〇一一年腊月廿九(2012-01-22)    1
二〇一二年正月初一(2012-01-23) - 二〇一二年腊月廿九(2013-02-09)    2
二〇一三年正月初一(2013-02-10) - 二〇一三年腊月三十(2014-01-30)    0
二〇一四年正月初一(2014-01-31) - 二〇一四年腊月三十(2015-02-18)    2
二〇一五年正月初一(2015-02-19) - 二〇一五年腊月廿九(2016-02-07)    1
二〇一六年正月初一(2016-02-08) - 二〇一六年腊月三十(2017-01-27)    0
二〇一七年正月初一(2017-01-28) - 二〇一七年腊月三十(2018-02-15)    2
二〇一八年正月初一(2018-02-16) - 二〇一八年腊月三十(2019-02-04)    1
二〇一九年正月初一(2019-02-05) - 二〇一九年腊月三十(2020-01-24)    0
二〇二〇年正月初一(2020-01-25) - 二〇二〇年腊月三十(2021-02-11)    2
二〇二一年正月初一(2021-02-12) - 二〇二一年腊月廿九(2022-01-31)    0
二〇二二年正月初一(2022-02-01) - 二〇二二年腊月三十(2023-01-21)    1
二〇二三年正月初一(2023-01-22) - 二〇二三年腊月三十(2024-02-09)    2
二〇二四年正月初一(2024-02-10) - 二〇二四年腊月廿九(2025-01-28)    0
二〇二五年正月初一(2025-01-29) - 二〇二五年腊月廿九(2026-02-16)    2
二〇二六年正月初一(2026-02-17) - 二〇二六年腊月廿九(2027-02-05)    1
 
...
```

