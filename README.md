# Borax - python3工具库 - 中国农历/中文数字/设计模式/树形结构


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
![Python package](https://github.com/kinegratii/borax/workflows/Python%20package/badge.svg)
![Codecov](https://codecov.io/github/kinegratii/borax/coverage.svg)
![GitHub license](https://img.shields.io/github/license/kinegratii/borax)
[![borax](https://snyk.io/advisor/python/borax/badge.svg)](https://snyk.io/advisor/python/borax)


## 概述 (Overview)

> github  https://github.com/kinegratii/borax
>
> gitee  https://gitee.com/kinegratii/borax



Borax 是一个Python3工具集合库。包括了以下几个话题：

| 话题（Topics）      | 内容                                                  |
| ------------------- | ----------------------------------------------------- |
| Borax.LunarDate     | 1900-2100年的中国农历日期库                           |
| Borax.Festivals     | 实现常见节日（公历、农历、星期、节气）的工具库                           |
| Borax.Choices       | 声明式的选项类。适用于Django.models.choices 定义。    |
| Borax.Datasets      | 记录型数据操作库，包括连结（Join）、列选择（fetch）等 |
| Borax.DataStuctures | 树形结构，json数据                                    |
| Borax.Numbers       | 数字库。包括中文数字、百分数等。                      |
| Borax.Patterns      | 设计模式。包括单例模式、代理对象、延迟对象。          |

## 安装 (Installation)

Borax 的 python 版本要求如下

| borax 版本 | python版本 |
| ------ | ------ |
| 4.x | 3.7+ |
| 3.x | 3.5+ |

可以通过 *pip* 安装 ：

```shell
$ pip install borax
```

## 版本 (Version)

Borax的版本符合 [语义化版本](https://semver.org/lang/zh-CN/) ，格式为 `<主版本号>.<副版本号>.<修正版本号>`， 推荐使用下面方式定义Borax的依赖版本号。

```text
borax~=3.5
```

## 使用示例 (Usage)

### Borax.LunarDate: 中国农历日期

一个支持1900-2100年的农历日期工具库。

> 本模块的数据和算法参考自项目 [jjonline/calendar.js](https://github.com/jjonline/calendar.js) 。

创建日期，日期推算

```python
from datetime import timedelta
from borax.calendars import LunarDate

# 获取今天的农历日期（农历2018年七月初一）
print(LunarDate.today()) # LunarDate(2018, 7, 1, 0)

# 将公历日期转化为农历日期
ld = LunarDate.from_solar_date(2018, 8, 11)
print(ld) # LunarDate(2018, 7, 1, 0)

# 日期推算，返回10天后的农历日期
print(ld.after(10)) # LunarDate(2018, 7, 11, 0)

# 可以直接与 datetime.timedelta 直接相加减
print(ld + timedelta(days=10)) # LunarDate(2018, 7, 11, 0)
```

格式化字符串

```python
today = LunarDate.today()
print(today.strftime('%Y年%L%M月%D')) # '二〇一八年六月廿六'
print(today.strftime('今天的干支表示法为：%G')) # '今天的干支表示法为：戊戌年庚申月辛未日'
```

### Borax.Festival: 国内外节日

创建春节（每年正月初一）对应的节日对象

```python
from borax.calendars.festivals2 import LunarFestival

festival = LunarFestival(month=1, day=1)
print(festival.description) # '农历每年正月初一'

# 下一次春节的具体日期以及距离天数
print(festival.countdown()) # (273, <GeneralDate:2022-02-01(二〇二二年正月初一)>)

# 接下来5个春节的日期 ['2022-02-01(二〇二二年正月初一)', '2023-01-22(二〇二三年正月初一)', '2024-02-10(二〇二四年正月初一)', '2025-01-29(二〇二五年正月初一)', '2026-02-17(二〇二六年正月初一)']
print([str(wd) for wd in festival.list_days(start_date=date.today(), count=5)])
```

### 可支持的节日类型

| 节日                          | 表示法                                                | 规范化描述                |
| ----------------------------- | ----------------------------------------------------- | ------------------------- |
| 元旦                          | SolarFestival(month=1, day=1)                         | 农历每年正月初一          |
| 中秋节                        | LunarFestival(month=8, day=15)                        | 农历每年八月十五          |
| 母亲节（每年5月第二个周日）   | WeekFestival(month=5, index=2, week=calendar.SUNDAY)  | 公历每年5月第2个星期日    |
| 除夕             | LunarFestival(day=-1)                                 | 农历每年最后一天          |
| 程序员节                      | SolarFestival(freq=FreqConst.YEARLY，day=256)         | 公历每年第256天           |
| 清明节                        | TemFestival(name="清明")                              | 公历每年清明              |
| 每月5日                       | SolarFestival(freq=FreqConst.MONTHLY， day=5)         | 公历每月5日               |
| 国际麻风节       | WeekFestival(month=1, index=-1, week=calendar.SUNDAY) | 公历1月倒数第1个星期日    |
| 每月最后一个周日 | WeekFestival(month=0, index=-1, week=calendar.SUNDAY) | 公历每月倒数第1个星期日   |
| 初伏 | TemFestival('夏至', nth=3, day_gz='庚') | 公历每年夏至起第三个庚日   |

### Borax.FestivalLibrary：内置节日库

基本使用示例

```python
from datetime import date
from borax.calendars.festivals2 import FestivalLibrary, WrappedDate

library = FestivalLibrary.load_builtin()

# 2020年国庆节和中秋节是同一天
names = library.get_festival_names(date(2020, 10, 1))
print(names) # ['国庆节', '中秋节']

# 2021年七夕
festival = library.get_festival('七夕')
print(festival.description) # '农历每年七月初七'
print(WrappedDate(festival.at(year=2021))) # '2021-08-14(二〇二一年七月初七)'
```

计算节日及其距离今天（2021年5月4日）的天数

```python

from borax.calendars.festivals2 import FestivalLibrary

library = FestivalLibrary.load_builtin()
for ndays, wd, festival in library.list_days_in_countdown(countdown=365):
    print(f'{ndays:>3d} {wd} {festival.name}')
```

输出结果

```
  0 2022-05-04(四月初四) 青年节
  4 2022-05-08(四月初八) 母亲节
  8 2022-05-12(四月十二) 护士节
...
332 2023-04-01(闰二月十一) 愚人节
336 2023-04-05(闰二月十五) 清明
362 2023-05-01(三月十二) 劳动节

```


### Borax.Numbers: 中文数字处理


不同形式的中文数字

```python
from borax.numbers import ChineseNumbers

# 小写、计量
print(ChineseNumbers.measure_number(204)) # '二百零四'
# 小写、编号
print(ChineseNumbers.order_number(204)) # '二百〇四'
# 大写、计量
print(ChineseNumbers.measure_number(204, upper=True)) # '贰佰零肆'
# 大写、编号
print(ChineseNumbers.order_number(204, upper=True)) # '贰佰〇肆'
```

财务金额

```python
import decimal

from borax.numbers import FinanceNumbers

decimal.getcontext().prec = 2

print(FinanceNumbers.to_capital_str(100000000)) # '壹亿元整'
print(FinanceNumbers.to_capital_str(4578442.23)) # '肆佰伍拾柒万捌仟肆佰肆拾贰元贰角叁分'
print(FinanceNumbers.to_capital_str(107000.53)) # '壹拾万柒仟元伍角叁分'
print(FinanceNumbers.to_capital_str(decimal.Decimal(4.50))) # '肆元伍角零分'
```

更多模块功能参见文档。

## 文档 (Document)

文档由 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建，另外备用文档使用 [docsify](https://docsify.js.org/) 构建。

| 源 | 网址 |
| ---- | ---- |
| read-the-docs | [https://borax.readthedocs.io/zh_CN/latest/](https://borax.readthedocs.io/zh_CN/latest/) |
| github | [https://kinegratii.github.io/borax](https://kinegratii.github.io/borax) |
| gitee | [https://kinegratii.gitee.io/borax](https://kinegratii.gitee.io/borax) |

## 开发特性和规范 (Development Features)

- [x] [Typing Hints](https://www.python.org/dev/peps/pep-0484/)
- [x] [Flake8 Code Style](http://flake8.pycqa.org/en/latest/)
- [x] [nose2](https://pypi.org/project/nose2/) | [pytest](https://docs.pytest.org/en/latest/)
- [x] [Github Action](https://github.com/kinegratii/borax/actions)
- [x] [Code Coverage](https://codecov.io/)
- [x] [pyproject.toml build tools](https://packaging.python.org/)

## 项目构建 (Project Build)

从4.0.1开始，borax 使用 *pyproject.toml* 作为项目构建的配置文件，使用以下命令构建 wheel 发行包。

```shell
python -m build -w
```

## 开源协议 (License)

The MIT License (MIT)

