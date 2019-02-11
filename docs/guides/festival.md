# festivals 模块

> 模块： `borax.calendars.festivals`

## 常用节日函数


- `iter_festival_countdown(countdown:Optional[int]=None, today:Union[date, LunarDate]） -> Iterator[int, List]`

计算节日距离某一日期还有多少天，结果按倒计天数分组。

```
>>>from borax.calendars.festivals import iter_festival_countdown
>>>list(iter_festival_countdown(30))
[(7, ['春节']), (16, ['情人节']), (21, ['元宵节'])]
```

- `get_festival(name:str) -> DateSchema`

获取一个节日的所代表日期对象(DateSchema)。

```
>>>from borax.calendars.festivals import get_festival
>>>festival = get_festival('春节')
>>>festival.countdown()
7
```

## 日期模式类(DateSchema)

### 定义

在 Borax 中，`DateSchema` 表示一个节日和生日的模式，其内部使用长度为10的数字字符串存储。

```
      SYYYYMMDDX
```

其中左起第1位为模式类型，根据该位的值决定其他字符划分、解析方式。每个模式使用 `DateSchema` 的一个子类表示，这些子类有一些具有相同意义的参数，

- year等于0表示一个模糊日期模式，可匹配任何一年的日期。
- name表示名称、标签，传入任何字符串即可。

每个子类也都有一些自己的参数，具体如下：

- **`SolarSchema(month, day, year=YEAR_ANY, reverse=0, **kwargs)`**

公历日期，比如元旦(1月1日)、劳动节(5月1日)、国庆节(10月1日)等。

当 reverse 等于0时，day 表示具体的“日”；当 reverse 等于1时，day 表示倒数的序数。

比如 reverse=1和day=1表示该月的最后一天，即1月31日、3月31日、4月30日...12月31日等。

- **`WeekSchema(month, index, week, year=YEAR_ANY, **kwargs)`**

依赖于星期的公历日期，比如母亲节(5月的第2个星期日)、父亲节、感恩节等。

星期的数值表示参考 `calendar` 模块的定义，即0表示星期一，6表示星期日。

比如 `WeekSchema(month=5, index=2, week=6)` 表示母亲节。

- **`TermSchema(index, year=YEAR_ANY, **kwargs)`**

依赖于节气的公历日期，比如清明、冬至。节气按照公历一年先后排序，即0为小寒、1为大寒、6为清明、23为冬至。

- **`LunarSchema(month, day, year=YEAR_ANY, leap=0, ignore_leap=1, **kwargs)`**

农历日期，比如七夕(七月初七)、腊八节 （腊月初八）等。

ignore_leap表示是否忽略闰月进行匹配。比如：
 
 (1)  `LunarSchema(month=6, day=1)` 可以匹配 `LunarDate(2017, 6, 1, 0)` 和 `LunarDate(2017, 6, 1, 1)` 两个日期。
 
 (2) `LunarSchema(month=6, day=1, ignore_leap=0)` 只匹配 `LunarDate(2017, 6, 1, 0)` 一个日期。
 
 (3) `LunarSchema(month=6, day=1, leap=1, ignore_leap=1)` 只匹配 `LunarDate(2017, 6, 1, 1)` 一个日期。

- **`DayLunarSchema(month, day, year=YEAR_ANY, reverse=0, **kwargs)`**

依赖具体日的农历日期，除夕(农历十二月的最后一天)。

当 reverse 等于0时，day 表示具体的“日”；当 reverse 等于1时，day 表示倒数的序数。

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
