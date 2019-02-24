# birthday 模块

> 模块：`borax.calendars.birthday`

`birthday` 模块提供了三种常用的年龄计算方法。

## 年龄API

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