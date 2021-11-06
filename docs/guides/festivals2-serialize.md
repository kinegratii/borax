# 日期节日序列化

> 模块： `borax.calendars.festivals2`

> Add in 3.5.0



## 概述

Borax.Calendars 实现了日期和节日的序列化和持久化，将表示日期或节日的python对象转化为特定格式的字符串存储在外部文件、数据库，也可以通过网络传输对象（如RPC调用）。

下面是一些简单的示例：

| 节日 | 序列化格式 | 节日 | 序列化格式 | 节日 | 序列化格式 |
| ----- | ----- | ----- | ----- | ----- | ----- |
| 元旦 | 001010 | 劳动节 | 005010 | 国庆节 | 010010 |
| 春节 | 101010 | 中秋节 | 108150 | 母亲节 | 205026 |
| 感恩节 | 211043 | 除夕 | 312011 | 清明 | 400060 |
| 2021元旦 | 0202101010 | 2021年劳动节 |  0202105050 | 2021年正月初一 | 1202101010 |
| 2020年闰四月十五 | 1202004151 | - |  - | - | - |

其中日期使用10位编码表示、节日使用6位编码表。日期字符串编码的第2-5位表示年份信息，其他字段的意义和节日字段相同。

Borax.Calendars 使用类似下列接口实现序列化和反序列化。

```python
class EncodeMixin:
    def encode(self) -> str:
        pass
    @classmethod
    def decode(cls, raw:str) -> 'cls':
        pass
```

下表是 `festivals2` 模块中实现该接口的日期节日对象。

| 日期节日类    | 描述                               |
| ------------- | ---------------------------------- |
| WrappedDate   | 公历日期、农历日期                 |
| Festival      | 节日的基类                         |
| SolarFestival | 公历节日，如元旦、劳动节、程序员节 |
| LunarFestival | 农历节日，如除夕、中秋节           |
| WeekFestival  | 公历星期节日，如母亲节、感恩节     |
| TermFestival  | 节气型节日，如清明、冬至           |
|               |                                    |

和 `festivals` 相比， `festivals2` 不再支持 `LunarDate` 的序列化，必须转化为对应的 `WrappedDate` 对象。这一特定将在Borax3.6版本移除。

## 使用方法

序列化方法定义在三个模块方法。

### encode

```python
festivals2.encode(obj: Union[WrappedDate, Festival]) -> str
```

序列化日期或节日对象，返回特定格式的字符串。

### decode

```python
festivals2.decode(raw: Union[str, bytes]) -> Union[WrappedDate, Festival]
```

反序列化日期或节日对象，返回 `WrappedDate` 或 `Festival` 对象。

### decode_festival

```python
festivals2.decode_festival(raw: Union[str, bytes]) -> Festival
```

反序列化节日对象，返回 `Festival` 对象。

## 基本定义

### 编码格式

基本的编码格式如下：

```
<1位schema> [<4位year>] <2位month> <2位day> <1位标志>
```

一些节日在此基础上进行了修改，参见下面的各子Festival的定义。

### FestivalSchema

第一位表示日期/节日类型，具体的对应关系如下：

| 首位取值 | 节日类        | 备注       |
| -------- | ------------- | ---------- |
| 0        | SolarFestival / WrappedDate |            |
| 1        | LunarFestival / WrapedDate |            |
| 2        | WeekFestival  |            |
| 3        | LunarFestival / WrappedDate | 兼容旧版本DayLunarSchema，只作解析，不作编码 |
| 4        | TermFestival |  |

### EncoderFlag

`SolarFestival` 和 `LunarFestival` 的最后一位表示标志位。

flag 字段使用聚合布尔值表示若干个标志的取值。

flag 的取值范围为0-F，标志值对应关系如下：

| flag取值 | day年序号 | 是否每月 | 是否倒序 | 是否闰月 |                          |
| -------- | --------- | -------- | -------- | -------- | ------------------------ |
| 0        | 0         | 0        | 0        | 0        | 月序号，每年，正序，平月 |
| 1        | 0         | 0        | 0        | 1        | 月序号，每年，正序，闰月 |
| 2        | 0         | 0        | 1        | 0        | 月序号，每年，倒序，平月 |
| 3        | 0         | 0        | 1        | 1        | 月序号，每年，倒序，闰月 |
| 4        | 0         | 1        | 0        | 0        | 月序号，每月，正序，平月 |
| 5        | 0         | 1        | 0        | 1        | 月序号，每月，正序，闰月 |
| 6        | 0         | 1        | 1        | 0        | 月序号，每月，倒序，平月 |
| 7        | 0         | 1        | 1        | 1        | 月序号，每月，倒序，闰月 |
| 8        | 1         | 0        | 0        | 0        | 年序号，每年，正序，平月 |
| 9        | 1         | 0        | 0        | 1        | 年序号，每年，正序，闰月 |
| A        | 1         | 0        | 1        | 0        | 年序号，每年，倒序，平月 |
| B        | 1         | 0        | 1        | 1        | 年序号，每年，倒序，闰月 |
| C        | 1         | 1        | 0        | 0        | 年序号，每月，正序，平月 |
| D        | 1         | 1        | 0        | 1        | 年序号，每月，正序，闰月 |
| E        | 1         | 1        | 1        | 0        | 年序号，每月，倒序，平月 |
| F        | 1         | 1        | 1        | 1        | 年序号，每月，倒序，闰月 |

## 日期序列化

### WrappedDate

| 字段（偏移量） | type(1)  | year(4)   | month(2) | day(2) | flag(1) |
| -------------- | -------- | --------- | -------- | ------ | ------- |
| 描述           | 节日类型 | 年份      | 月份     | 日期   | 标志位  |
| 取值范围       | 0(公历)  | 1900-2100 | 01-12    | 01-31  | 0       |
|                | 1(农历)  | 1900-2100 | -        | 01-30  | 0-1     |

公历农历日期。

- 当type=1表示农历日期，此时flag表示是否是农历闰月。

## 节日序列化

### SolarFestival

| 字段（偏移量） | type(1)  | month(2) | day(2)    | flag(1) |
| -------------- | -------- | -------- | --------- | ------- |
| 描述           | 节日类型 | 月份     | 日期      | 标志位  |
| 取值范围       | 0        | 01-12    | 01-31     | 0-7     |
|                | 0        | -        | 0000-0366 | 8-F     |

公历型节日。

- 当 flag 取4-7 时，编码第2-5位共同表示一个day字段。

### LunarFestival

| 字段（偏移量） | type(1)  | month(2) | day(2)    | flag(1) |
| -------------- | -------- | -------- | --------- | ------- |
| 描述           | 节日类型 | 月份     | 日期      | 标志位  |
| 取值范围       | 1        | 01-12    | 01-31     | 0-7    |
|                | 1        | -        | 0000-0384 | 8-F  |
|                 | 3       | 00-12      | 01-31 | 0-1     |

农历型节日。

- 当 type = 1 且 flag 取4-7 时，编码第2-5位共同表示一个day字段。
- type = 3时为兼容旧版本之用，此时 0 表示（每年,正序,平月），1表示（每年,倒序,平月）

### WeekFestival

| 字段（偏移量） | type(1)  | month(2) | index(2) | week(1) |
| -------------- | -------- | -------- | -------- | ------- |
| 描述           | 节日类型 | 月份     | 序号     | 星期    |
| 取值范围       | 2        | 01-12    | 01-05    | 0-6     |

星期型节日。

### TermFestival

| 字段（偏移量） | type(1)  | -(2) | index(2) | -(1) |
| -------------- | -------- | ---- | -------- | ---- |
| 描述           | 节日类型 | -    | 节气序号 | -    |
| 取值范围       | 4        | 00   | 00-23    | 0    |

节气型节日。

- 节气序号（index ）按照公历一年先后排序，即0为小寒、1为大寒、6为清明、23为冬至。

## FestivalLibrary类

### load_file

```python
load_file(cls, file_path: Union[str, Path]) -> 'FestivalLibrary'
```

从文件加载节日列表，返回FestivalLibrary对象。

### load_builtin

```python
FestivalLibrary.load_builtin(cls, identifier: str = 'zh-Hans') -> 'FestivalLibrary'
```

从默认文件加载节日列表，返回FestivalLibrary对象。

### get_festival

```python
get_festival(name: str) -> Optional[Festival]
```

根据名称获取 Festival对象。

### get_festival_names

```python
get_festival_names(date_obj: MixedDate) -> list
```

获取某一个具体日期的节日名称，返回节日名称。

### iter_festival_countdown

```python
iter_festival_countdown(countdown: Optional[int] = None, date_obj: MixedDate = None) -> Iterator[Tuple[int, List]]
```

计算节日距离某一日期还有多少天，结果按倒计天数分组。

```python
list(factory.iter_festival_countdown(30)) # [(7, ['春节']), (16, ['情人节']), (21, ['元宵节'])]
```

### decode

```python
festivals2.decode(raw:str)->Festival
```

将字符串编码解析为 `Festival` 对象，如果无法解析将抛出 `ValueError ` 异常。

 