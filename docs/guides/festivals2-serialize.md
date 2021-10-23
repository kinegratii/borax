# Festivals2序列化

本节描述了 `Festival` 的序列化，通过序列化操作可以将 `Festival` 对象以字符串形式保存在文件等持久化存储之中。如下图：

```
001010,元旦
005010,劳动节
005040,青年节
010010,国庆节
101010,春节
108150,中秋节
205026,母亲节
211043,感恩节
312011,除夕
400060,清明
```

## 编码规则

### 长短编码

根据是否包含“年份”信息，可分为6位的短编码形式和10位的长编码形式，长编码的第2-5位表示年份信息。

### FestivalSchema

第一位表示节日类型，可区分具体的 `Festival` 类，具体的对应关系如下：

| 首位取值 | 节日类        | 备注       |
| -------- | ------------- | ---------- |
| 0        | SolarFestival |            |
| 1        | LunarFestival  |            |
| 2        | WeekFestival  |            |
| 3        | LunarFestival | 兼容旧版本DayLunarSchema，只作解析，不作编码 |
| 4        | TermFestival |  |

### EncoderFlag

flag 字段使用聚合布尔值表示若干个的标志，适用于 `SolarFestival` 和 `LunarFestival` 的序列化。

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

 

### SolarFestival

| 字段（偏移量） | type(1)  | month(2) | day(2)    | flag(1) |
| -------------- | -------- | -------- | --------- | ------- |
| 描述           | 节日类型 | 月份     | 日期      | 标志位  |
| 取值范围       | 0        | 01-12    | 01-31     | 0-7     |
|                | 0        | -        | 0000-0366 | 6-F     |

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

 