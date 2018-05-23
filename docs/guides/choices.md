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
import ConstChoices

class Student(models.Model):
    class GenderChoices(ConstChoices.ConstChoices):
        MALE = ConstChoices.Item(1, 'male')
        FEMALE = ConstChoices.Item(2, 'female')
        UNKOWN = ConstChoices.Item(3, 'unkown')
        
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