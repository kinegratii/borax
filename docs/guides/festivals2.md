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
 
### 异常类
 
 
- `festivals2.FestivalError（label, message）`
 
 
异常类。
 

### 模块类
 
 
所有类如下：
 
 
- Festival：表示特定的节日类，该类为抽象类，具体的节日类参见 *节日定义* 一节。
- FestivalError：异常类
- FestivalLibrary：节日库

## 基础数据结构
 
 
### WrappedDate：通用日期类
 
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
 
`WrappedDate` 也支持日期的计算。原则是 **只要操作数中有一个是WrappedDate对象，结果就是WrappedDate对象**。
 
| 左操作数         | 操作符 | 右操作数         | 结果        |              |
| ---------------- | ------ | ---------------- | ----------- | ------------ |
| WrappedDate      | +      | timedelta        | WrappedDate | `w.__add__`  |
| timedelta        | +      | WrappedDate      | WrappedDate | `w.__radd__` |
| date / LunarDate | -      | WrappedDate      | timedelta   | d.sub/l.sub  |
| WrappedDate      | -      | date / LunarDate | timedelta   | w.sub        |
| WappedDate       | -      | timedelta        | WappedDate  | w.sub        |
 
 
 
 
### Period：期间工具类
 
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
 
### 创建节日对象

节日是对日期（公历和农历）的进一步抽象。
 
| 节日                        | 表示法                                               | 规范化描述             |
| --------------------------- | ---------------------------------------------------- | ---------------------- |
| 元旦                        | SolarFestival(month=1, day=1)                        | 农历每年正月初一       |
| 中秋节                      | LunarFestival(month=8, day=15)                       | 农历每年八月十五       |
| 母亲节（每年5月第二个周日） | WeekFestival(month=5, index=2, week=calendar.SUNDAY) | 公历每年5月第2个星期日 |
| 除夕                        | LunarFestival(month=12, day=-1)                      | 农历每年腊月最后一天   |
|                             | LunarFestival(day=-1)                                | 农历每年最后一天       |
| 程序员节                    | SolarFestival(freq=YEARLY，day=256)                  | 公历每年第256天        |
| 清明节                      | TemFestival(name="清明")                             | 公历每年清明           |
| 每月5日                     | SolarFestival(freq=MONTHLY， day=5)                  | 公历每月5日            |
|                             |                                                      |                        |

 
festivals模块使用4个类表示节日，各个类的初始化函数签名如下：

 
```python
class SolarFestival(day, freq=YEARLY, year=0, month=0)
class WeekFestival(month, index, week)
class TermFestival(name)
class LunarFestival(day, freq=YEARLY, year=0, month=0, leap=0)
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
 
### 其他属性
 
**`Festival.set_name(name)`**
 
设置节日对象的 name。
 
## 基于单日期的方法
 
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
 
方法签名
 
```python
Festival.is_(date_obj:MixedDate) -> bool
```
 
判断给定的日期是否是该节日，返回布尔值。
 
 
| 新版                                        | 旧版    | 功能                               |
| ------------------------------------------- | ------- | ---------------------------------- |
| `is_(date_obj)`                             | match   | 判定给定的日期是否是该节日         |
| `at(year)`                                  | reslove | 根据year获取节日，如果没有返回None |
| `list_days(start_date, end_date, **kwargs)` |         | 遍历日期                           |
| `list_days(solar_year)`                     |         |                                    |
| `list_days(solar_year, solar_month)`        |         |                                    |
|                                             |         |                                    |
 
### 示例
 
代码
 
```python
from datetime import datetime, date
import calendar
from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals2 import LunarFestival, WeekFestival
# 构建除夕节对象日，农历12月的最后一天
chuxi = LunarFestival(month=12, day=-1, name="除夕")
 
chuxi_of_this_year = chuxi.at(year=2021)
 
 
montherDay = WeekFestival(month=5, index=2, week=calendar.SUNDAY, name="母亲节")
 
montherDayForThisYear = montherDay.at(year=2021)
 
nextMonthDay = montherDay.list_days(start_date=datetime.now())[0]
 
ld = LunarDate(year=2020, month=12, day=30)
 
print(chuxi.is_(ld)) # True
 
next_chuxi_list = [ld for ld in chuxi.iter_days(start_date=date.today())]
```
 
## 节日迭代
 
 
### iter_days
 
方法签名
 
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
# 方案二
chuxi = LunarFestival(month=12, day=-1)
for wd in chuxi.list_days(*Period.future()):
    sd, ld = wd
    print("%s %s".format(sd.strftime("%y-%m-%d"), ld.cn_str()))
```
 
### list_days
 
```python
Festival.list_days(start_date=None, end_date=None, reverse=False, count=-1)
```
 
返回在 start_date 和 end_date 之间（含起止日期）匹配本 Festival 的日期列表。
 
- start_date, end_date, reverse 的参数意义同 iter_days 方法
- 返回一个日期列表。
- count表示日期列表的长度。
 
### 其他方法
 
 
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
 
 
## 综合使用示例
 
### 除夕日列表
 
 
 
```python
chuxi = LunarFestival(month=12, day=-1)
for day in chuxi.list_days(start_date=date.today()):
    sd = day.to_solar_date()
    print("%s %s".format(sd.strftime("%y-%m-%d %h:%i:%s"), day.cn_str()))
```
 
 
 
###  两头春、无头春
 
```python
# 农历两头春，无头春
 
 
# 在农历year年时间段，立春的个数
tf = TermFestival(name='立春')
for year in range(MIN_LUNAR_YEAR, MAX_LUNAR_YEAR):
    start_date, end_date = Period.lunar_year(year)
    ncount = len(list(tf.list_days(start_date, end_date)))
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
 
## 附录：开发性接口变更
 
 
 
- `Festival.list_days` 移除 reverse 参数
- `LCalendars.cast` 支持 `GeneralDate` 参数
- 模块变量 YEARLY/MONTHLY 变为 Freq类变量
- 内部方法 `Festival._resolve` 统一返回 `List[Union[date, LunarDate]]`
- 移除`Festival.list_in_period`
- 移除短编码字符串
- `SolarSchema`、`LunarSchema` 的 day 参数允许取负值，表示倒数。
- DayLunarSchema 移除
 
 
## 附录：新旧API对比
 
体系结构
 
| 旧版API        | 新版API       | 变化 |
| -------------- | ------------- | ---- |
| SolarSchema    | SolarFestival |      |
| WeekSchema     | WeekFestival  |      |
| TermSchema     | TermFestival  |      |
| LunarSchema    | LunarFestival |      |
| DayLunarSchema |               |      |
 
 
 
 