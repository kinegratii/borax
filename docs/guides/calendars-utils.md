# 日期工具库

Borax.Calendars 提供了一系列适用于常见场景的工具方法。这些方法都定义在 `borax.calendars.SCalendars` （公历相关）和 `borax.calendars.LCalendars` （农历相关）类中。



## 公历工具SCalendars

> Add in v3.4.0

- `SCalendars.get_last_day_of_this_month(year: int, month: int) -> date`

返回year年month月的最后一天日期。

- `SCalendars.get_fist_day_of_year_week(year: int, week: int) -> date`

返回year年第week个星期第一天的日期。

## 三伏数九天 - ThreeNineUtils

> Add in v3.5.1

三伏天的描述如下：

我国传统的推算方法规定，夏至以后的第３个庚日、第４个庚日分别为初伏（头伏）和中伏的开始日期，立秋以后的第一个庚日为末伏的第一天。因为每个庚日之间相隔１０天，所以初伏、末伏规定的时间是１０天。又因为每年夏至节气后的第３个庚日（初伏）出现的迟早不同，中伏的天数就有长有短，可能是１０天，也可能是２０天。

数九的描述如下：

从冬天的冬至算起（冬至即一九第1天），每九天为一"九"，第一个九天叫做"一九"，第二个九天叫"二九"，依此类推，数到"九九"八十一天。

### API

`ThreeNineUtils` 类提供了有关三伏数九的计算函数。

- **ThreeNineUtils.get_39label(date_obj: Union[date, LunarDate]) -> str**

返回某一个日期的相关标签，该标签格式为“初伏/中伏/末伏/一九/二九/.../八九/九九第x天”。如果不是，则返回空字符串。

```python
from datetime import date
from borax.calendars.utils import ThreeNineUtils
print(ThreeNineUtils.get_39label(date(2021, 7, 21))) # '中伏第1天'
```

- **ThreeNineUtils.get_39days(year: int) -> Dict[str, date]**

返回某一个公历年份的三伏数九天起始日期的全部信息，如 `ThreeNineUtils.get_39days(2021)` 的返回值如下：

```pythonconsole
{'一九': datetime.date(2021, 12, 21),
 '七九': datetime.date(2022, 2, 13),
 '三九': datetime.date(2022, 1, 8),
 '中伏': datetime.date(2021, 7, 21),
 '九九': datetime.date(2022, 3, 3),
 '二九': datetime.date(2021, 12, 30),
 '五九': datetime.date(2022, 1, 26),
 '八九': datetime.date(2022, 2, 22),
 '六九': datetime.date(2022, 2, 4),
 '初伏': datetime.date(2021, 7, 11),
 '四九': datetime.date(2022, 1, 17),
 '末伏': datetime.date(2021, 8, 20)}

```

