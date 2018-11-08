# choices 模块

> 模块： `borax.choices`

## 基本使用

继承自 `choices.ConstChoices`, 并使用 `choices.Item` 列出所有的可选项。

```python
from borax import choices

class YearInSchoolChoices(choices.ConstChoices):
    FRESHMAN = choices.Item('FR', 'Freshman')
    SOPHOMORE = choices.Item('SO', 'Sophomore')
    JUNIOR = choices.Item('JR', 'Junior')
    SENIOR = choices.Item('SR', 'Senior')
```

 ```bash
 >>> YearInShoolChoices.FRESHMAN
'FR'
>>> YearInShoolChoices.is_valid('SR')
True
>>> YearInShoolChoices.is_valid('Et')
False
```
## 选项定义

在类定义体使用 `<name> = <value>` 的格式定义选项。

名称 name 遵循 Python 命名规范，但需要注意的是以下划线（"_"）开始的变量不视为一个有效的选项。

值 value 支持以下几种形式：

- `choices.Item` 对象
- 含有2个元素的列表或元组
- 一个单值对象

在一个 `ConstChoices` 定义中，以下四个语句是等效的：

```
NS = choices.Item('A', 'A')
NS = choices.Item('A')
NS = 'A', 'A'
NS = 'A'
```


例如上述 `YearInSchoolChoices` 也可以简写为

```python
class YearInSchoolChoices(choices.ConstChoices):
    FRESHMAN = 'FR', 'Freshman'
    SOPHOMORE = 'SO', 'Sophomore'
    JUNIOR = 'JR', 'Junior'
    SENIOR = 'SR', 'Senior'
```

## 整合到 Django

未使用 `borax.choices` 时：

```python
from django.db import models

class Student(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    UNKOWN = 'unkown'
    
    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'famale'),
        (UNKOWN, 'unkown')
    )
    gender = models.IntergerFIeld(
        choices=GENDER_CHOICES,
        default=UNKOWN
    )
```

使用后：

```python
from django.db import models
from borax import choices

class GenderChoices(choices.ConstChoices):
    MALE = choices.Item(1, 'male')
    FEMALE = choices.Item(2, 'female')
    UNKOWN = choices.Item(3, 'unkown')
    
class Student(models.Model):        
    gender = models.IntergerFIeld(
        choices=GenderChoices,
        default=GenderChoices.UNKOWN
    )

```

## 方法 API

> 以下所有的方法均为 `ConstChoices` 类方法，

- **`ConstChoices.choices`**

所有选项列表。可直接用于 django.models.Field.choices 。

类似于 `[(value1, display1), (value2, display2), ...]` 。

- **`ConstChoices.is_valid(value)`**

检查 `value` 是否是有效的选项。

- **`ConstChoices.get_value_display(value)`**

获取某个选项的文本。