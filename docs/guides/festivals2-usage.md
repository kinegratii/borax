# 农历与节日

## 引言

Borax是一个比较完备的python农历库，覆盖了农历、闰月、干支、节日等内容。相关代码模块如下：

- borax.calendars.lunardate 农历日期
- borax.calendars.festivals2 节日及其序列化
- borax.calendars.utils 包含工具函数

## 农历日期

### 创建新日期

一个农历日期由年份、月份、日期、闰月标记等组成，依次传入这四个属性就可以创建一个农历日期对象。

```python
from borax.calendars.lunardate import LunarDate

ld = LunarDate(2022,4,1,0)
print(ld) # LunarDate(2022, 4, 1, 0)
```

正如 `datetime.date` 一样， `LunarDate.strftime` 提供了日期字符串格式化功能。

```python
print(ld.strftime('%Y年%L%M月%D')) # '二〇二二年四月初一'
print(ld.strftime('%G')) # '壬寅年甲辰月甲寅日'
```

### 日期推算

`LunarDate` 被设计为不可变对象，可以作为字典的key使用，也可以比较大小。

`LunarDate` 也可以和 `date` 、`timedelta` 进行日期大小计算。

```python
ld2 = ld + timedelta(days=10)
print(ld) # LunarDate(2022, 4, 11, 0)
```

### 传统日期

`TermUtils` 支持从特定的节气按照干支的顺序计算日期。如初伏、出梅。节气隶属于公历系统，相关函数返回值为 `datetime.date`。

```python
dz2022 = TermUtils.day_start_from_term(2022, '冬至') # 计算2022年的冬至是那一天
print(dz2022) # 2022-12-22

day13 = TermUtils.day_start_from_term(2022, '夏至', 3, '庚') # 初伏：夏至起第3个庚日
print(day13) # 2022-07-16
```



## 农历闰月

### 闰月计算

为了协调回归年与农历年的矛盾，防止农历年月与回归年即四季脱节，每19年置7闰。Borax提供了一系列有关闰月的计算方法。

判断某个月份是否是闰月。

```python
from borax.calanders.lunardate import LCalendars

print(LCalendars.leap_month(2020) == 3) # False；2020年3月不是闰月
print(LCalendars.leap_month(2020) == 4) # True；2020年4月是闰月
print(LCalendars.leap_month(2023) == 2) # True；2023年2月也是闰月
```

获取有某个闰月的年份。

```python
# 在1900~2100两百年中只有2033年是闰十一月
print(LCalendars.get_leap_years(11)) # (2033, )

# 在1900~2100两百年没有闰正月的情况
print(LCalendars.get_leap_years(1)) # ( )
```

某个农历月份的天数，（29天为小月，30天为大月）。

```python
# 农历2022年四月小，五月大
print(LCalendars.ndays(2022, 4)) # 29
print(LCalendars.ndays(2022, 5)) # 30
```

计算农历年的天数。

```python
# 2023年有闰二月。
print(LCalendars.ndays(2022)) # 355
print(LCalendars.ndays(2023)) # 384
```

### 打印闰月表

打印某个时间段内的闰月表：

```python
from borax.calendars.lunardate import TextUtils, LCalendars
for year in range(2021, 2050):
    leap_month = LCalendars.leap_month(year)
    if leap_month == 0:
        continue
    if LCalendars.ndays(year, leap_month, 1) == 30:
        label = '大'
    else:
        label = '小'
    print('{}年闰{}月{}'.format(year, TextUtils.MONTHS_CN[leap_month], label))
```

结果输出

```text
2023年闰二月小
2025年闰六月小
2028年闰五月小
2031年闰三月小
2033年闰冬月小
2036年闰六月大
2039年闰五月小
2042年闰二月小
2044年闰七月小
2047年闰五月大
```

## 节日

### 创建节日

`borax.calendars.festivals2` 模块包含了多种节日类（均继承自 `Festival`），这些类覆盖了大多数类型的公共和传统节日。

公历节日

```python
new_year = SolarFestival(month=1, day=1)
next_new_year = new_year.at(year=2022)
# 获取2022年的元旦日期
print(repr(next_new_year)) # datetime.date(2022, 1, 1)
# 今天是否是元旦
print(new_year.is_(date.today())) # False
```

农历除夕

```python
new_year_eve = LunarFestival(day=-1)  # 每年农历最后一天
next_eve = new_year_eve.at(year=2021)
print(repr(next_eve)) # LunarDate(2021, 12, 29, 0)
```

国际麻风节

```python
import calendar
from borax.calendars.festivals2 import WeekFestival

leprosy_festival = WeekFestival(
    month=1, index=-1, week=calendar.SUNDAY, name='国际麻风节'
)
print(leprosy_festival.description) # '公历1月最后1个星期日'
for w in leprosy_festival.list_days_in_future(count=5):
    print(w.simple_str())
```

### 日期列举

获取接下去10年的除夕日期

```python
new_year_eve = LunarFestival(day=-1)
for ld in new_year_eve.list_days_in_future(count=10):
    print(ld)
```

输出结果：

```
2022-01-31(二〇二一年腊月廿九)
2023-01-21(二〇二二年腊月三十)
2024-02-09(二〇二三年腊月三十)
2025-01-28(二〇二四年腊月廿九)
2026-02-16(二〇二五年腊月廿九)
2027-02-05(二〇二六年腊月廿九)
2028-01-25(二〇二七年腊月廿九)
2029-02-12(二〇二八年腊月廿九)
2030-02-02(二〇二九年腊月三十)
2031-01-22(二〇三〇年腊月廿九)
```

## 综合示例

### 两头春

两头春：一个农历年中，有两个立春。无春年，一个农历年没有立春。

```python
from borax.calendars.festivals2 import Period, TermFestival, WrappedDate
licun = TermFestival('立春')

for lunar_year in range(2000, 2030):
    star_date, end_date = Period.lunar_year(lunar_year)
    festival_days = licun.list_days(star_date, end_date)
    line = '{} {}-{} {} | {}'.format(
        lunar_year,
        WrappedDate(star_date).simple_str(),
        WrappedDate(end_date).simple_str(),
        len(festival_days),
        ' '.join([str(wd) for wd in festival_days])
    )
    print(line)
```

结果输出

```text
2000 2000-02-05(正月初一)-2001-01-23(腊月廿九) 0 |
2001 2001-01-24(正月初一)-2002-02-11(腊月三十) 2 | 2001-02-04(正月十二) 2002-02-04(腊月廿三)
2002 2002-02-12(正月初一)-2003-01-31(腊月廿九) 0 |
2003 2003-02-01(正月初一)-2004-01-21(腊月三十) 1 | 2003-02-04(正月初四)
2004 2004-01-22(正月初一)-2005-02-08(腊月三十) 2 | 2004-02-04(正月十四) 2005-02-04(腊月廿六)
2005 2005-02-09(正月初一)-2006-01-28(腊月廿九) 0 |
2006 2006-01-29(正月初一)-2007-02-17(腊月三十) 2 | 2006-02-04(正月初七) 2007-02-04(腊月十七)
2007 2007-02-18(正月初一)-2008-02-06(腊月三十) 1 | 2008-02-04(腊月廿八)
2008 2008-02-07(正月初一)-2009-01-25(腊月三十) 0 |
2009 2009-01-26(正月初一)-2010-02-13(腊月三十) 2 | 2009-02-04(正月初十) 2010-02-04(腊月廿一)
2010 2010-02-14(正月初一)-2011-02-02(腊月三十) 0 |
2011 2011-02-03(正月初一)-2012-01-22(腊月廿九) 1 | 2011-02-04(正月初二)
2012 2012-01-23(正月初一)-2013-02-09(腊月廿九) 2 | 2012-02-04(正月十三) 2013-02-04(腊月廿四)
2013 2013-02-10(正月初一)-2014-01-30(腊月三十) 0 |
2014 2014-01-31(正月初一)-2015-02-18(腊月三十) 2 | 2014-02-04(正月初五) 2015-02-04(腊月十六)
2015 2015-02-19(正月初一)-2016-02-07(腊月廿九) 1 | 2016-02-04(腊月廿六)
2016 2016-02-08(正月初一)-2017-01-27(腊月三十) 0 |
2017 2017-01-28(正月初一)-2018-02-15(腊月三十) 2 | 2017-02-03(正月初七) 2018-02-04(腊月十九)
2018 2018-02-16(正月初一)-2019-02-04(腊月三十) 1 | 2019-02-04(腊月三十)
2019 2019-02-05(正月初一)-2020-01-24(腊月三十) 0 |
2020 2020-01-25(正月初一)-2021-02-11(腊月三十) 2 | 2020-02-04(正月十一) 2021-02-03(腊月廿二)
2021 2021-02-12(正月初一)-2022-01-31(腊月廿九) 0 |
2022 2022-02-01(正月初一)-2023-01-21(腊月三十) 1 | 2022-02-04(正月初四)
2023 2023-01-22(正月初一)-2024-02-09(腊月三十) 2 | 2023-02-04(正月十四) 2024-02-04(腊月廿五)
2024 2024-02-10(正月初一)-2025-01-28(腊月廿九) 0 |
2025 2025-01-29(正月初一)-2026-02-16(腊月廿九) 2 | 2025-02-03(正月初六) 2026-02-04(腊月十七)
2026 2026-02-17(正月初一)-2027-02-05(腊月廿九) 1 | 2027-02-04(腊月廿八)
2027 2027-02-06(正月初一)-2028-01-25(腊月廿九) 0 |
2028 2028-01-26(正月初一)-2029-02-12(腊月廿九) 2 | 2028-02-04(正月初十) 2029-02-03(腊月二十)
2029 2029-02-13(正月初一)-2030-02-02(腊月三十) 0 |
```

