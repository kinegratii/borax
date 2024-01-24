# festivals2 模块

> 模块： `borax.calendars.festivals2`

> Updated in 4.1.0：新增 Festival.code属性。

> Updated in 3.5.6: 星期型节日(WeekFestival)类支持倒数序号。如：“国际麻风节(1月最后一个星期天)”

> Updated in 3.5.6: 星期型节日(WeekFestival)类支持每月频率。

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

| 参数  | 描述                                                         | 取值           |
| ----- | ------------------------------------------------------------ | -------------- |
| freq  | 节日频率，“每年”或“每月”，默认“每年”。                       | 0:每年；1:每月 |
| month | 月份。                                    | 0,1-12         |
| day   | 日期序号。当month取值0时，表示一年的第几天；否则表示该月的第几天。允许取负值，表示一年/一个月的倒数 第几天。 |                |

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

| 参数  | 描述                                                         | 取值            |
| ----- | ------------------------------------------------------------ | --------------- |
| freq  | 节日频率，“每年”或“每月”，默认“每年”。                       | 0:每年；1:每月  |
| month | 月份。                                                       | 0,1-12          |
| leap  | 闰月标记。取值参见 `LeapConst`。                             | LeapConst.MIXED |
| day   | 日期序号。当month未设置时，表示一年的第几天；否则表示该月的第几天。允许取负值，表示一年/一个月的倒数 第几天。 |                 |

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

返回今后时间（[today, end_date]）之间（含起止日期）匹配本 Festival 的日期列表。

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

## FestivalLibrary：节日集合库

`FestivalLibrary` 是集合容器类，提供了一些常用的节日。此类继承自 `collections.UserList` ，拥有  append/remove/extend/insert等方法。

需要注意的是，`FestivalLibrary` 并不重写这些方法的逻辑，因此如需保证节日不重复，可以使用 `extend_unique` 方法添加。

```python
class FestivalLibrary(collections.UserList):
    pass
```

创建一个节日库对象主要有三种方法：

第一，从 borax 提供默认数据加载。

```python
fl = FestivalLibrary.load_builtin('basic') # 加载基础节日库，可选 empty / basic / ext1
```

第二，从某个 csv 文件加载。

```python
fl = FestivalLibrary.load_file('/usr/amy/festivals/my_festival.csv')
```

第三，从已有的节日创建新的节日库。

```python
fl1 = FestivalLibrary(fl) # 复制 fl节日库

# 使用函数式编程过滤其中的公历型节日
fl2 = FestivalLibrary(filter(lambda f: f.schema == FestivalSchema.SOLAR, fl)) 
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

### extend_term_festivals

> Add in v4.0.1

```
FestivalLibrary.extend_term_festivals()
```

添加24个节气节日。

### delete_by_indexes

> Add in v4.0.0

```python
FestivalLibrary.delete_by_indexes(indexes:List[int])
```

按照位置删除多个元素。

### load_file

```python
FestivalLibrary.load_file(cls, file_path: Union[str, Path]) -> 'FestivalLibrary'
```

从文件 file_path 中加载节日数据。

### load_builtin

```python
FestivalLibrary.load_builtin(cls, identifier: str = 'basic') -> 'FestivalLibrary'
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

### list_days_in_countdown

> Add in 3.5.6
>
> Update in v4.0.0:新增 countdown_ordered 参数。如果为False，按节日原顺序输出。

```python
FestivalLibrary.list_days_in_countdown(countdown: Optional[int] = None, date_obj: MixedDate = None,  countdown_ordered: bool = True
    ) -> List[Tuple[int, WrappedDate, Festival]]
```

迭代获取某个时间的倒计时信息。

计算节日及其距离今天（2021年5月4日）的天数

```python

from borax.calendars.festivals2 import FestivalLibrary

library = FestivalLibrary.load_builtin()
for ndays, wd, festival in library.list_days_in_countdown(countdown=365):
    print(f'{ndays:>3d} {wd} {festival.name}')
```

输出结果

```
  0 2022-05-04(四月初四) 青年节
  4 2022-05-08(四月初八) 母亲节
  8 2022-05-12(四月十二) 护士节
...
332 2023-04-01(闰二月十一) 愚人节
336 2023-04-05(闰二月十五) 清明
362 2023-05-01(三月十二) 劳动节
```

### iter_festival_countdown

> Deprecated in 3.5.6: 可使用 `list_days_in_countdown` 方法。

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
  7 儿童节 2021-06-01(四月廿一)
 20 端午节 2021-06-14(五月初五)
 26 父亲节 2021-06-20(五月十一)
...
344 青年节 2022-05-04(四月初四)
348 母亲节 2022-05-08(四月初八)
352 护士节 2022-05-12(四月十二)
```

### iter_month_daytuples

> Updated in 3.5.5: 新增 `return_pos` 参数

> Added in 3.5.2

```python
FestivalLibrary.iter_month_daytuples(year: int, month: int, firstweekday: int = 0, return_pos:bool = False)
```

迭代返回公历月份（含前后完整日期）中每个日期信息，每个日期格式为 `(公历日, 农历日中文或节日, WrappedDate对象)`。

如果 return_pos 设置为 True，则返回 `(公历日, 农历日中文或节日, WrappedDate对象, 行序号, 列序号)`。

例子
```python
import pprint
from borax.calendars.festivals2 import FestivalLibrary

library = FestivalLibrary.load_builtin()
days = list(library.iter_month_daytuples(2022,1, return_pos=True))
pprint.pprint(days)
```

输出结果

```
[(0, '', None, 0, 0),
 (0, '', None, 0, 1),
 (0, '', None, 0, 2),
 (0, '', None, 0, 3),
 (0, '', None, 0, 4),
 (1, '元旦', <WrappedDate:2022-01-01(二〇二一年冬月廿九)>, 0, 5),
 (2, '三十', <WrappedDate:2022-01-02(二〇二一年冬月三十)>, 0, 6),
 (3, '十二月', <WrappedDate:2022-01-03(二〇二一年腊月初一)>, 1, 0),
 (4, '初二', <WrappedDate:2022-01-04(二〇二一年腊月初二)>, 1, 1),
 (5, '小寒', <WrappedDate:2022-01-05(二〇二一年腊月初三)>, 1, 2),
 (6, '初四', <WrappedDate:2022-01-06(二〇二一年腊月初四)>, 1, 3),
 (7, '初五', <WrappedDate:2022-01-07(二〇二一年腊月初五)>, 1, 4),
 (8, '初六', <WrappedDate:2022-01-08(二〇二一年腊月初六)>, 1, 5),
 (9, '初七', <WrappedDate:2022-01-09(二〇二一年腊月初七)>, 1, 6),
 (10, '腊八节', <WrappedDate:2022-01-10(二〇二一年腊月初八)>, 2, 0),
 (11, '初九', <WrappedDate:2022-01-11(二〇二一年腊月初九)>, 2, 1),
 (12, '初十', <WrappedDate:2022-01-12(二〇二一年腊月初十)>, 2, 2),
 (13, '十一', <WrappedDate:2022-01-13(二〇二一年腊月十一)>, 2, 3),
 (14, '十二', <WrappedDate:2022-01-14(二〇二一年腊月十二)>, 2, 4),
 (15, '十三', <WrappedDate:2022-01-15(二〇二一年腊月十三)>, 2, 5),
 (16, '十四', <WrappedDate:2022-01-16(二〇二一年腊月十四)>, 2, 6),
 (17, '十五', <WrappedDate:2022-01-17(二〇二一年腊月十五)>, 3, 0),
 (18, '十六', <WrappedDate:2022-01-18(二〇二一年腊月十六)>, 3, 1),
 (19, '十七', <WrappedDate:2022-01-19(二〇二一年腊月十七)>, 3, 2),
 (20, '大寒', <WrappedDate:2022-01-20(二〇二一年腊月十八)>, 3, 3),
 (21, '十九', <WrappedDate:2022-01-21(二〇二一年腊月十九)>, 3, 4),
 (22, '二十', <WrappedDate:2022-01-22(二〇二一年腊月二十)>, 3, 5),
 (23, '廿一', <WrappedDate:2022-01-23(二〇二一年腊月廿一)>, 3, 6),
 (24, '廿二', <WrappedDate:2022-01-24(二〇二一年腊月廿二)>, 4, 0),
 (25, '廿三', <WrappedDate:2022-01-25(二〇二一年腊月廿三)>, 4, 1),
 (26, '廿四', <WrappedDate:2022-01-26(二〇二一年腊月廿四)>, 4, 2),
 (27, '廿五', <WrappedDate:2022-01-27(二〇二一年腊月廿五)>, 4, 3),
 (28, '廿六', <WrappedDate:2022-01-28(二〇二一年腊月廿六)>, 4, 4),
 (29, '廿七', <WrappedDate:2022-01-29(二〇二一年腊月廿七)>, 4, 5),
 (30, '廿八', <WrappedDate:2022-01-30(二〇二一年腊月廿八)>, 4, 6),
 (31, '除夕', <WrappedDate:2022-01-31(二〇二一年腊月廿九)>, 5, 0),
 (0, '', None, 5, 1),
 (0, '', None, 5, 2),
 (0, '', None, 5, 3),
 (0, '', None, 5, 4),
 (0, '', None, 5, 5),
 (0, '', None, 5, 6)]

```

### monthdaycalendar

> Added in 3.5.2

```python
FestivalLibrary.monthdaycalendar(year: int, month: int, firstweekday: int = 0)
```

返回二维列表，每一行表示一个星期。逻辑同iter_month_daytuples。

### to_csv

> Add in 3.5.6

```python
FestivalLibrary.to_csv(path_or_buf)
```

保存到 csv 文件。

### filter_inplace

> Add in 4.0.0

```
FestivalLibrary.filter_(**kwargs)
```

按条件过滤节日，保留符合参数条件的节日，返回实例本身。

可用的参数条件

| 参数名称              | 参数值类型 | 描述               |
| --------------------- | ---------- | ------------------ |
| schema                | int        | 节日类型值         |
| schema__in            | List[int]  | 多个节日类型值     |
| catalog               | str        | 节日分类标签       |
| catalog__in           | List[str]  | 多个节日分类标签   |
| name                  | str        | 名称，精确匹配     |
| name__in              | List[str]  | 多个名称           |
| name__contains        | str        | 节日名称，模糊匹配 |
| description           | str        | 节日描述           |
| description__contains | str        | 节日描述，模糊匹配 |

### exclude_inplace

> Add in 4.0.0

```
FestivalLibrary.exclude_(**kwargs)
```

按条件过滤节日，符合参数条件的节日将会被删除，返回实例本身。

### filter_

按条件过滤节日条目，保留符合参数条件的节日，返回新的 `FestivalLibray` 实例。

### exclude_

按条件过滤节日，符合参数条件的节日将会被删除，返回新的 `FestivalLibray` 实例。

### sort_by_countdown

> Add in 4.0.0

```
FestivalLibrary.sort_by_countdown(reverse=False)
```

按照距离今天的倒计天数 **原地排序**，返回实例本身。







