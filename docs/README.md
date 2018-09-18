# Borax


[![PyPI](https://img.shields.io/pypi/v/borax.svg)](https://pypi.org/project/borax) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/borax.svg)](https://pypi.org/project/borax)
[![PyPI - Status](https://img.shields.io/pypi/status/borax.svg)](https://github.com/kinegratii/borax)




## 概述

Borax 是一个的 Python3 开发工具集合库,涉及到：

 - 设计模式示例
 - 数据结构

## 安装

Borax 要求 Python 的版本至少为 3.5 以上。可以通过以下三种方式安装 Borax ：

1) 使用 *pip* ：

```shell
$ pip install borax
```
2) 使用 [poetry](https://poetry.eustace.io/) 工具：

```shell
$ poetry add borax
```

3) 使用开发代码

```shell
git clone https://github.com/kinegratii/borax.git
cd borax
python setup.py install
```


## 版本

打印 Borax 的版本。

```python
from borax import __version__
print(__version__)
```