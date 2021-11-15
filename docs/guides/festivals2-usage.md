# festivals2综合示例

> 模块： `borax.calendars.festivals2`

> Add in 3.5.0

## 常规日期

公历节日

```python
new_year = SolarFestival(month=1, day=1)
next_new_year = new_year.at(year=2022)
# 获取2022年的元旦日期
print(repr(next_new_year)) # datetime.date(2022, 1, 1)
# 今天是否是元旦
print(new_year.is_(date.today())) # False
```

农历“除夕”

```python
new_year_eve = LunarFestival(month=12, day=-1)  # 每年农历十二月最后一天
next_eve = new_year_eve.at(year=2021)
print(repr(next_eve)) # LunarDate(2021, 12, 29, 0)
```

冬至节日

```python
tf = TermFestival(name='冬至')
dz = tf.at(year=2021)
print(repr(dz)) # datetime.date(2021, 12, 21)
```



## 日期列举

获取接下去10年的除夕日期

```python
new_year_eve = LunarFestival(month=12, day=-1)
for ld in new_year_eve.list_days(start_date=LunarDate.today(), count=10):
    print(ld)
```

结果

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

## sqlite3整合

`festival2` 内置了对sqlite3数据库自定义字段的支持。在示例中可以在同一个字段存储公历生日日期和农历生日日期。

```python
import sqlite3

from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals2 import encode, decode, WrappedDate

sqlite3.register_adapter(WrappedDate, encode)
sqlite3.register_converter("WrappedDate", decode)

con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
cur.execute('CREATE TABLE member (pid INT AUTO_INCREMENT PRIMARY KEY,birthday WrappedDate);')
ld = LunarDate(2018, 5, 3)
cur.execute("INSERT INTO member(birthday) VALUES (?)", (WrappedDate(ld),))
cur.execute("SELECT pid, birthday FROM member;")
my_birthday = cur.fetchone()[1]
cur.close()
con.close()
print(my_birthday)
```
