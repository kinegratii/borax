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

### lunardate

> The dataset and algorithm is referenced from [jjonline/calendar.js](https://github.com/jjonline/calendar.js).

Get the date instance of today.

```
>>>from borax.calendars.lunardate import LunarDate
>>>LunarDate.today()
LunarDate(2018, 7, 1, 0)
>>>ld = LunarDate.from_solar_date(2018, 8, 11)
>>>ld
LunarDate(2018, 7, 1, 0)
>>>ld.after(10)
LunarDate(2018, 7, 11, 0)
```

### Choices

Use `choices` in django models.

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

This project is issued with MIT License, see LICENSE file for more detail.