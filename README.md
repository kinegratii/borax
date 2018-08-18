# Borax


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
[![PyPI - Status](https://img.shields.io/pypi/status/borax.svg)](https://github.com/kinegratii/borax)




## 概述

Borax 是一个的 Python3 开发工具集合库,涉及到：

 - 设计模式示例
 - 数据结构
 - 常用工具

## 安装

Borax 要求 Python 的版本至少为 3.5 以上。

使用 *pip* ：

```shell
$ pip install borax

```

或者使用开发代码

```shell
git clone https://github.com/kinegratii/borax.git
cd borax
python setup.py install
```

## 模块用法示例

### Choices 模块

在 django models 中使用 `choices` 。

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

### Fetch

从数据序列中选择一个或多个字段的数据。

```python
from borax.fetch import fetch

objects = [
    {'id': 282, 'name': 'Alice', 'age': 30},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56},
]

names = fetch(objects, 'name')
print(names)
```

输出

```
['Alice', 'Bob', 'Charlie']
```

## 文档

在线文档托管在 [https://kinegratii.github.io/borax](https://kinegratii.github.io/borax) ，由 [docsify](https://docsify.js.org/) 构建。

## 开源协议

```
The MIT License (MIT)

Copyright (c) 2015-2018 kinegratii

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```