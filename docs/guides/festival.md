# festivals 模块

> 模块： `borax.calendars.festivals`

> Update in 4.0.0: 本模块已被移除。
>
> 本模块已经标记为 废弃 状态，请使用 `festivals2` 模块。

## 日期模式类(DateSchema)

在 Borax.Calendars 中，使用 `DateSchema` 表示和定义一个节假日、生日等日期，称之为 **日期模式** 。日期模式是与年份无关的，在给定的年份中，可以计算推导出一个或多个具体的日期。

由于节日的表示各不相同，有的是农历日期，有的是公历日期，也有的是按星期确定具体的日期，每个表示形式（模式）使用 `DateSchema` 的一个子类表示。

`DateSchema` 仅提供了一些简单的接口，无法被实例化。

- year等于0表示一个模糊日期模式，可匹配任何一年的日期。
- name表示名称、标签，传入任何字符串即可。

### SolarSchema

- **`SolarSchema(month, day, year=YEAR_ANY, reverse=0, **kwargs)`**

公历日期，比如元旦(1月1日)、劳动节(5月1日)、国庆节(10月1日)等。

当 reverse 等于0时，day 表示具体的“日”；当 reverse 等于1时，day 表示倒数的序数。

比如 reverse=1和day=1表示该月的最后一天，即1月31日、3月31日、4月30日...12月31日等。

节日编码表示如下：

| 字段(长度) | schema(1) | year(4) | month(2) | day(2) | reverse(1) |
| ------ | ------ | ------ | ------ | ------ | ------ |
| 描述 | 模式序号 | 年份 | 月份 | 日期或序号 | 是否倒序 |
| 取值范围 | 0 | 0000,1900 - 2101 | 01 - 12 | 01 - 31 | 0,1 |

### WeekSchema

- **`WeekSchema(month, index, week, year=YEAR_ANY, **kwargs)`**

依赖于星期的公历日期，比如母亲节(5月的第2个星期日)、父亲节、感恩节等。

星期的数值表示参考 `calendar` 模块的定义，即0表示星期一，6表示星期日。

比如 `WeekSchema(month=5, index=2, week=6)` 表示母亲节。

节日编码表示如下：

| 字段(长度) | schema(1) | year(4) | month(2) | index(2) | week(1) |
| ------ | ------ | ------ | ------ | ------ | ------ |
| 描述 | 模式序号 | 年份 | 月份 | 序号 | 星期 |
| 取值范围 | 2 | 0000,1900 - 2101 | 01 - 12 | 01 - 05 | 0 - 6 |

### TermSchema

- **`TermSchema(index, year=YEAR_ANY, **kwargs)`**

依赖于节气的公历日期，比如清明、冬至。节气按照公历一年先后排序，即0为小寒、1为大寒、6为清明、23为冬至。

节日编码表示如下：

| 字段(长度) | schema(1) | year(4) | - (2) | index(2) | - (1) |
| ------ | ------ | ------ | ------ | ------ | ------ |
| 描述 | 模式序号 | 年份 | - | 节气序号 | - |
| 取值范围 | 4 | 0000,1900 - 2101 | 00 | 01 - 23 | 0 |


### LunarSchema

- **`LunarSchema(month, day, year=YEAR_ANY, leap=0, ignore_leap=1, **kwargs)`**

农历日期，比如七夕(七月初七)、腊八节 （腊月初八）等。

ignore_leap表示是否忽略闰月进行匹配。比如：

 (1)  `LunarSchema(month=6, day=1)` 可以匹配 `LunarDate(2017, 6, 1, 0)` 和 `LunarDate(2017, 6, 1, 1)` 两个日期。

 (2) `LunarSchema(month=6, day=1, ignore_leap=0)` 只匹配 `LunarDate(2017, 6, 1, 0)` 一个日期。

 (3) `LunarSchema(month=6, day=1, leap=1, ignore_leap=1)` 只匹配 `LunarDate(2017, 6, 1, 1)` 一个日期。

节日编码表示如下：

| 字段(长度) | schema(1) | year(4) | month(2) | day(2) | leap(1) |
| ------ | ------ | ------ | ------ | ------ | ------ |
| 描述 | 模式序号 | 年份 | 月份 | 日期 | 是否闰月 |
| 取值范围 | 1 | 0000,1900 - 2100 | 01 - 12 | 01 - 30 | 0,1 |

### DayLunarSchema

- **`DayLunarSchema(month, day, year=YEAR_ANY, reverse=0, **kwargs)`**

依赖具体日的农历日期，比如除夕(农历十二月的最后一天)。

当 reverse 等于0时，day 表示具体的“日”；当 reverse 等于1时，day 表示倒数的序数。

节日编码表示如下：

| 字段(长度) | schema(1) | year(4) | month(2) | day(2) | reverse(1) |
| ------ | ------ | ------ | ------ | ------ | ------ |
| 描述 | 模式序号 | 年份 | 月份 | 日期或序号 | 是否倒序 |
| 取值范围 | 3 | 0000,1900 - 2100 | 01 - 12 | 01 - 30 | 0,1 |

### 方法

> 以下函数的 `date_obj` 参数可以传入 `datetime.date` 或者 `LunarDate` 对象。

- **DateSchema.match(data_obj:Union[date, LunarDate]) -> bool**

返回 date_obj 的日期和 所代表节日的是否是同一天。

```
>>> from datetime import date
>>>from borax.calendars.festivals import SolarSchema
>>>md = SolarSchema(year=0, month=2, day=14)
>>>md.match(date(2020, 2, 14))
True
```

- **DateSchema.countdown(data_obj:Union[date, LunarDate]) -> int**

返回 data_obj 的日期和本节日下一次日期的距离天数。

```
>>>from borax.calendars.lunar import LunarDate
>>>from borax.calendars.festivals import LunarSchema
>>>ls = LunarSchema(year=0, month=4, day=2)
>>>ls.countdown(LunarDate(2019, 4, 1))
1
```

- **DateSchema.resolve(year:int) -> Union[date, LunarDate]**

获取某年该日期模式对应的日期对象，具体类型由 `DateSchema.data_class` 确定。

```
>>>from borax.calendars.festivals import LunarSchema
>>>ls = LunarSchema(year=0, month=4, day=2)
>>>ls.resolve(2019)
LunarDate(2019, 4, 2)
```

- **DateSchema.delta(date_obj:Union[date, LunarDate]) -> int**

  获取和 date_obj 距离的天数，要求 `DateSchema.year` 不为0。

```
>>>from borax.calendars.festivals import LunarSchema
>>>ls = LunarSchema(year=0, month=4, day=2)
>>>ls.delta()
-6550
```

## 序列化和存储

`DateSchema` 实现了 `Encoder` 的接口，可以在 `DateSchema` 和字符串之间进行转换， 支持不同形式节日的混合存储。

节日编码字符串有长短两种形式。长编码字符串的长度为10，包含了年份字段；短编码字符串长度为6，不包含年份字段。

```
DateSchema    ====(encode)====>    RawString

RawString     ====(decode)====>    DateSchema
```

- **DateSchema.encode(short: bool = True) -> str**

转化为编码字符串，这是一个实例方法。

- classmethod **DateSchema.decode(raw) -> DateSchema**

根据编码字符串创建模式对象，这是一个类方法。


例子：

```python
from datetime import date
from borax.calendars.festivals import SolarSchema

ss = SolarSchema.decode('0000012310')
print(ss.match(date(2018, 12, 31))) # True
```

## 节日计算工具(FestivalFactory)

`FestivalFactory`类支持从特定的外部文件读取一系列的节日信息。

```
class FestivalFactory(lang=None, file_path=None)
```

`festivals` 也内置了一些国家地区常见的节假日，可以通过 lang 读取这些信息。

```python
from datetime import date
from borax.calendars.festivals import FestivalFactory

factory = FestivalFactory(lang='zh-Hans')
festival = factory.get_festival('元旦')
print(festival.match(date(2018, 1, 1))) # True
```

`FestivalFactory` 提供了一系列函数。

- `iter_festival_countdown(countdown:Optional[int]=None, today:Union[date, LunarDate], lang: str = 'zh-Hans'） -> Iterator[int, List]`

计算节日距离某一日期还有多少天，结果按倒计天数分组。

```python
list(factory.iter_festival_countdown(30)) # [(7, ['春节']), (16, ['情人节']), (21, ['元宵节'])]
```

- `get_festival(name:str, lang: str = 'zh-Hans') -> DateSchema`

获取一个节日的所代表日期对象(DateSchema)。

```python
festival = factory.get_festival('春节')
festival.countdown() # 7
```

## 快捷访问工具

为了保持之前的兼容性，`festivals` 提供了几个快捷函数。调用这些函数无需创建相应的 `FestivalFactory` 实例 。

- `iter_festival_countdown(countdown:Optional[int]=None, today:Union[date, LunarDate]） -> Iterator[int, List]`
- `get_festival(name:str) -> DateSchema`
