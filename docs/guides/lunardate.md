# lunardate 模块

> 模块： `borax.calendars.lunardate`

本模块代码基于 [python-lunardate](https://github.com/lidaobing/python-lunardate) 修改，使用 GPLv2 开源协议发布。

- 农历日期上限支持到 2100 年
- 添加 Typing Hints
- 优化部分代码

## LunarDate类

一个 `LunarDate` 对象代表一个农历日期。

```python
class LunarDate(year:int, month:int, day:int, isLeapMonth:bool)
```

各个参数的意义如下：

- year ：整数，农历年份，范围为 1900 - 2100 。
- month ： 整数，农历月份，范围为 1 -12 。
- day ： 整数，农历日期，范围为 1 - 30 。
- isLeapMonth ： 布尔值，是否为农历闰月。

获取今天的农历日期对象。

```
>>>LunarDate.today()
LunarDate(2018, 6, 27, 0))
```

## 公历转化

- **classmethod LunarDate.fromSolarDate(year, month, day)**


从公历日期转化为农历日期。

```python
dt2 = LunarDate.fromSolarDate(2033, 10, 23)
print(dt2.year)
```

- **LunarDate.toSolarDate() -> datetime.date**

将当前日期转化为公历日期

## 日期加减

`LunarDate` 支持和 `datetime.timedelta` 进行加减计算，结果为一个新的 `LunarDate` 。例如：

```
>>> LunarDate(2018, 6, 3) + timedelta(days=3)
LunarDate(2018, 6, 6, 0)
```

两个 `LunarDate` 相加减的结果为一个 `timedelta` 对象。

```
>>> LunarDate(2018, 6, 18) - LunarDate(2018, 6, 3)
timedelta(days=15)
```


