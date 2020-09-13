# 日期工具库

> Add in v3.4.0

Borax.Calendars 提供了一系列适用于常见场景的工具方法。这些方法都定义在 `borax.calendars.SCalendars` （公历相关）和 `borax.calendars.LCalendars` （农历相关）类中。



## 公历工具SCalendars

- `SCalendars.get_last_day_of_this_month(year: int, month: int) -> date`

返回year年month月的最后一天日期。

- `SCalendars.get_fist_day_of_year_week(year: int, week: int) -> date`

返回year年第week个星期第一天的日期。



## 农历日期LCalendars

