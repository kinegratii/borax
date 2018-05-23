# Borax


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
[![PyPI - Status](https://img.shields.io/pypi/status/borax.svg)](https://github.com/kinegratii/borax)




## Overview

Borax is a utils collections for python3 development, which contains some common data structures and the implementation of design patterns.

## Installation

Borax requires Python3.5+ .

Use *pip* :

```shell
$ pip install borax

```

Or checkout source code:

```shell
git clone https://github.com/kinegratii/borax.git
cd borax
python setup.py install
```

## Modules Usage

### Choices

Use `choices` in django models.

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

### Fetch

A function sets for fetch the values of some axises.


Get list values from dict list.

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

Output

```
['Alice', 'Bob', 'Charlie']
```

## Document

See [online document](https://kinegratii.github.io/borax) for more detail, which is powered by [docsify](https://docsify.js.org/) .

## License

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