# 节日集合库(FestivalLibrary)

> 模块: borax.calendars.festivals2

> Add in 3.5.0

## 数据格式

节日库 FestivalLibrary 是由众多节日组成的数据库，可保存为 csv 文件，csv文件格式如下：

```
<节日编码>,<节日名称>,<节日标签>
```

或

```
<节日编码>,<节日名称>
```

文件的每一行可代表一个 `Festival` 对象，依次对应于 code、name、labels三个属性。

例子：

```csv
001010,元旦
002140,情人节
003080,妇女节
003120,植树节
004010,愚人节
005010,劳动节
```

## Borax内置节日库

Borax内置了两个节日库，位于 `borax.calendars.datasets` 包下。

| 标识  | 文件               | 描述       | 备注                             |
| ----- | ------------------ | ---------- | -------------------------------- |
| basic | FestivalData.csv   | 基础节日   | 节气节日仅包括清明、冬至两个节日 |
| ext1  | festivals_ext1.csv | 扩展的节日 |                                  |

可使用 `FestivalLibrary.load_buitin` 加载这些数据。

## API

`FestivalLibrary` 是集合容器类，提供了一些常用的节日。此类继承自 `collections.UserList` ，拥有  append/remove/extend/insert等方法。

需要注意的是，`FestivalLibrary` 并不重写这些方法的逻辑，因此如需保证节日不重复，可以使用 `extend_unique` 方法添加。

```python
class FestivalLibrary(collections.UserList):
    pass
```

创建一个节日库对象主要有三种方法：

第一，从 borax 提供默认数据加载。

```python
fl = FestivalLibrary.load_builtin('basic') # 加载基础节日库，可选 empty / basic / ext1
```

第二，从某个 csv 文件加载。

```python
fl = FestivalLibrary.load_file('/usr/amy/festivals/my_festival.csv')
```

第三，从已有的节日创建新的节日库。

```python
fl1 = FestivalLibrary(fl) # 复制 fl节日库

# 使用函数式编程过滤其中的公历型节日
fl2 = FestivalLibrary(filter(lambda f: f.schema == FestivalSchema.SOLAR, fl)) 
```

### get_code_set

> Add in v3.5.1

```
FestivalLibrary.get_code_set()
```

获取当前所有节日的code集合。

### extend_unique

> Add in v3.5.1

```
FestivalLibrary.extend_unique(other)
```

添加多个节日对象，类似于 extend 方法，但是如果code已经存在则不再加入。

### extend_term_festivals

> Add in v4.0.1

```
FestivalLibrary.extend_term_festivals()
```

添加24个节气节日。

### delete_by_indexes

> Add in v4.0.0

```python
FestivalLibrary.delete_by_indexes(indexes:List[int])
```

按照位置删除多个元素。

### load

> Add in 4.1.0

```python
FestivalLibrary.load(cls, identifier_or_path: Union[str, Path]) -> 'FestivalLibrary'
```

加载Borax内部数据或自定义文件。

```python
fl = FestivalLibrary.load('basic')

fl2 = FestivalLibrary.load('/usr/my/my_festivals.csv')
```



### load_file

```python
FestivalLibrary.load_file(cls, file_path: Union[str, Path]) -> 'FestivalLibrary'
```

从文件 file_path 中加载节日数据。

### load_builtin

```python
FestivalLibrary.load_builtin(cls, identifier: str = 'basic') -> 'FestivalLibrary'
```

加载Borax提供的节日库数据。

### get_festival

```python
FestivalLibrary.get_festival(self, name: str) -> Optional[Festival]
```

根据名称获取对应的 Festival 对象。

### get_festival_names

```python
FestivalLibrary.get_festival_names(self, date_obj: MixedDate) -> list
```

获取某一个日期的节日名称列表。

### list_days_in_countdown

> Add in 3.5.6
>
> Update in v4.0.0:新增 countdown_ordered 参数。如果为False，按节日原顺序输出。

```python
FestivalLibrary.list_days_in_countdown(countdown: Optional[int] = None, date_obj: MixedDate = None,  countdown_ordered: bool = True
    ) -> List[Tuple[int, WrappedDate, Festival]]
```

迭代获取某个时间的倒计时信息。

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

### iter_festival_countdown

> Deprecated in 3.5.6: 可使用 `list_days_in_countdown` 方法。

```python
FestivalLibrary.iter_festival_countdown(self, countdown: Optional[int] = None, date_obj: MixedDate = None) -> Iterator[Tuple[int, List]]
```

迭代获取节日的日期。

```python

from borax.calendars.festivals2 import FestivalLibrary

fl = FestivalLibrary.load_builtin()
for nday, gd_list in fl.iter_festival_countdown():
    for gd in gd_list:
        print('{:>3d} {} {}'.format(nday, gd.name, gd))

```

输出

```
  7 儿童节 2021-06-01(四月廿一)
 20 端午节 2021-06-14(五月初五)
 26 父亲节 2021-06-20(五月十一)
...
344 青年节 2022-05-04(四月初四)
348 母亲节 2022-05-08(四月初八)
352 护士节 2022-05-12(四月十二)
```

### iter_month_daytuples

> Updated in 3.5.5: 新增 `return_pos` 参数

> Added in 3.5.2

```python
FestivalLibrary.iter_month_daytuples(year: int, month: int, firstweekday: int = 0, return_pos:bool = False)
```

迭代返回公历月份（含前后完整日期）中每个日期信息，每个日期格式为 `(公历日, 农历日中文或节日, WrappedDate对象)`。

如果 return_pos 设置为 True，则返回 `(公历日, 农历日中文或节日, WrappedDate对象, 行序号, 列序号)`。

例子
```python
import pprint
from borax.calendars.festivals2 import FestivalLibrary

library = FestivalLibrary.load_builtin()
days = list(library.iter_month_daytuples(2022,1, return_pos=True))
pprint.pprint(days)
```

输出结果

```
[(0, '', None, 0, 0),
 (0, '', None, 0, 1),
 (0, '', None, 0, 2),
 (0, '', None, 0, 3),
 (0, '', None, 0, 4),
 (1, '元旦', <WrappedDate:2022-01-01(二〇二一年冬月廿九)>, 0, 5),
 (2, '三十', <WrappedDate:2022-01-02(二〇二一年冬月三十)>, 0, 6),
 (3, '十二月', <WrappedDate:2022-01-03(二〇二一年腊月初一)>, 1, 0),
 (4, '初二', <WrappedDate:2022-01-04(二〇二一年腊月初二)>, 1, 1),
 (5, '小寒', <WrappedDate:2022-01-05(二〇二一年腊月初三)>, 1, 2),
 (6, '初四', <WrappedDate:2022-01-06(二〇二一年腊月初四)>, 1, 3),
 (7, '初五', <WrappedDate:2022-01-07(二〇二一年腊月初五)>, 1, 4),
 (8, '初六', <WrappedDate:2022-01-08(二〇二一年腊月初六)>, 1, 5),
 (9, '初七', <WrappedDate:2022-01-09(二〇二一年腊月初七)>, 1, 6),
 (10, '腊八节', <WrappedDate:2022-01-10(二〇二一年腊月初八)>, 2, 0),
 (11, '初九', <WrappedDate:2022-01-11(二〇二一年腊月初九)>, 2, 1),
 (12, '初十', <WrappedDate:2022-01-12(二〇二一年腊月初十)>, 2, 2),
 (13, '十一', <WrappedDate:2022-01-13(二〇二一年腊月十一)>, 2, 3),
 (14, '十二', <WrappedDate:2022-01-14(二〇二一年腊月十二)>, 2, 4),
 (15, '十三', <WrappedDate:2022-01-15(二〇二一年腊月十三)>, 2, 5),
 (16, '十四', <WrappedDate:2022-01-16(二〇二一年腊月十四)>, 2, 6),
 (17, '十五', <WrappedDate:2022-01-17(二〇二一年腊月十五)>, 3, 0),
 (18, '十六', <WrappedDate:2022-01-18(二〇二一年腊月十六)>, 3, 1),
 (19, '十七', <WrappedDate:2022-01-19(二〇二一年腊月十七)>, 3, 2),
 (20, '大寒', <WrappedDate:2022-01-20(二〇二一年腊月十八)>, 3, 3),
 (21, '十九', <WrappedDate:2022-01-21(二〇二一年腊月十九)>, 3, 4),
 (22, '二十', <WrappedDate:2022-01-22(二〇二一年腊月二十)>, 3, 5),
 (23, '廿一', <WrappedDate:2022-01-23(二〇二一年腊月廿一)>, 3, 6),
 (24, '廿二', <WrappedDate:2022-01-24(二〇二一年腊月廿二)>, 4, 0),
 (25, '廿三', <WrappedDate:2022-01-25(二〇二一年腊月廿三)>, 4, 1),
 (26, '廿四', <WrappedDate:2022-01-26(二〇二一年腊月廿四)>, 4, 2),
 (27, '廿五', <WrappedDate:2022-01-27(二〇二一年腊月廿五)>, 4, 3),
 (28, '廿六', <WrappedDate:2022-01-28(二〇二一年腊月廿六)>, 4, 4),
 (29, '廿七', <WrappedDate:2022-01-29(二〇二一年腊月廿七)>, 4, 5),
 (30, '廿八', <WrappedDate:2022-01-30(二〇二一年腊月廿八)>, 4, 6),
 (31, '除夕', <WrappedDate:2022-01-31(二〇二一年腊月廿九)>, 5, 0),
 (0, '', None, 5, 1),
 (0, '', None, 5, 2),
 (0, '', None, 5, 3),
 (0, '', None, 5, 4),
 (0, '', None, 5, 5),
 (0, '', None, 5, 6)]

```

### monthdaycalendar

> Added in 3.5.2

```python
FestivalLibrary.monthdaycalendar(year: int, month: int, firstweekday: int = 0)
```

返回二维列表，每一行表示一个星期。逻辑同`iter_month_daytuples` 。

### to_csv

> Add in 3.5.6

```python
FestivalLibrary.to_csv(path_or_buf)
```

保存到 csv 文件。

### filter_inplace

> Add in 4.0.0

```
FestivalLibrary.filter_(**kwargs)
```

按条件过滤节日，保留符合参数条件的节日，返回实例本身。

可用的参数条件

| 参数名称              | 参数值类型 | 描述               |
| --------------------- | ---------- | ------------------ |
| schema                | int        | 节日类型值         |
| schema__in            | List[int]  | 多个节日类型值     |
| catalog               | str        | 节日分类标签       |
| catalog__in           | List[str]  | 多个节日分类标签   |
| name                  | str        | 名称，精确匹配     |
| name__in              | List[str]  | 多个名称           |
| name__contains        | str        | 节日名称，模糊匹配 |
| description           | str        | 节日描述           |
| description__contains | str        | 节日描述，模糊匹配 |

### exclude_inplace

> Add in 4.0.0

```
FestivalLibrary.exclude_(**kwargs)
```

按条件过滤节日，符合参数条件的节日将会被删除，返回实例本身。

### filter_

按条件过滤节日条目，保留符合参数条件的节日，返回新的 `FestivalLibray` 实例。

### exclude_

按条件过滤节日，符合参数条件的节日将会被删除，返回新的 `FestivalLibray` 实例。

### sort_by_countdown

> Add in 4.0.0

```
FestivalLibrary.sort_by_countdown(reverse=False)
```

按照距离今天的倒计天数 **原地排序**，返回实例本身。