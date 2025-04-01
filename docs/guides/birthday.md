# birthday 模块

> 模块：`borax.calendars.birthday`



> Add in v4.1.3：新增 `BirthdayCalculator` 类。

`birthday` 模块提供了常用的两种年龄计算方法。

| 年龄              | 说明                                                     |
| ----------------- | -------------------------------------------------------- |
| 虚岁(Nominal Age) | 在中国传统习俗，出生时即为 1 岁，每逢农历新年增加 1 岁。 |
| 周岁(Actual Age)  | 按公历计算，每过一个公历生日就长一岁。                   |

## 年龄API(对象式)

> New in v4.1.3

### 基本用法

从 v4.1.3 开始，本模块新增对象式的API，所涉及到类如下：

| 类                 | 描述                                  |
| ------------------ | ------------------------------------- |
| BirthdayCalculator | 计算器                                |
| BirthdayResult     | 计算得到的结果，为 `dateclass` 数据类 |

`BirthdayCalculator` 接受一个公历日期或农历日期，使用 `calculate` 方法计算相关结果。

```python
my_birthday = date(2000, 3, 4)
my_bc = BirthdayCalculator(my_birthday)
print(my_bc.birthday)
result = my_bc.calculate()
print(asdict(result))
```

结果

```text
2000-03-04(正月廿九)
{
    'nominal_age': 26,
    'actual_age': 25,
    'animal': '龙',
    'birthday_str': '2000-03-04(二〇〇〇年正月廿九)',
    'next_solar_birthday': <WrappedDate:2026-03-04(正月十六)>,
    'next_lunar_birthday': <WrappedDate:2026-03-17(正月廿九)>,
    'living_day_count': 9150
}
```

### BirthdayCalculator

**初始化**

```python
BirthdayCalculator(birthday: Union[date, LunarDate])
```

birthday 为某人的生日日期，接受公历和农历两种形式。

**计算生日相关信息**

```
BirthdayCalculator.calculate(this_day:Union[date, LuarDate]) -> BirthdayResult
```

以 this_day 为基准，计算周岁、虚岁、下一次生日等相关信息。`BirthdayResult` 相关信息如下：

```python
class BirthdayResult:
    nominal_age: int = 0  # 虚岁
    actual_age: int = 0  # 周岁
    animal: str = ''  # 生肖
    birthday_str: str = '' # 生日描述字符串
    next_solar_birthday: WrappedDate = None  # 下一次公历生日
    next_lunar_birthday: WrappedDate = None  # 下一次农历生日
    living_day_count: int = 0 # 总天数
```

**计算农历公历生日在同一天的日期**

```
BirthdayCalculator.list_days_in_same_day(start_date=None, end_date=None)->list[WrappedDate]
```

计算农历公历生日在同一天的日期。

## 年龄API(函数式)

> 这些函数式API已标记为废弃 deprecated，将在 4.2.0 版本移除。

### 虚岁

**nominal_age(birthday:MDate, today:MDate = None) -> int**

例子：

```python
from borax.calendars.lunardate import LunarDate
from borax.calendars.birthday import nominal_age

birthday = LunarDate(2017, 6, 16, 1)
print(nominal_age(birthday, LunarDate(2017, 6, 21, 1))) # 1
print(nominal_age(birthday, LunarDate(2017, 12, 29))) # 1
print(nominal_age(birthday, LunarDate(2018, 1, 1))) # 2
```

### 周岁（按公历）

**actual_age_solar(birthday:MDate, today:MDate = None) -> int**

例子：

```python
from datetime import date
from borax.calendars.birthday import actual_age_solar

print(actual_age_solar(date(2000, 2, 29), date(2003, 2, 28))) # 2
print(actual_age_solar(date(2000, 2, 29), date(2003, 3, 1))) # 3
```

### 周岁（按农历）

**actual_age_lunar(birthday:MDate, today:MDate = None) -> int**

例子：

```python
from datetime import date
from borax.calendars.birthday import actual_age_lunar

birthday = date(1983, 5, 20)

print(actual_age_lunar(birthday, today=date(2007, 5, 23))) # 23
actual_age_lunar(birthday, today=date(2007, 5, 24)) # 24
actual_age_lunar(birthday, today=date(2007, 5, 25)) # 24
```