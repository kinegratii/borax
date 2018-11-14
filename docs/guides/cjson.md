# cjson 模块

> 模块：`borax.serialize.cjson`

`cjson` 是一个基于 [singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch) 的json 序列化工具。

一般来说，使用 `cjson.to_serializable.register` 装饰器，为自定义的类绑定一个序列化函数。


```python
import json

from borax.serialize import cjson

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@cjson.to_serializable.register(Point)
def encode_point(o):
    return [o.x, o.y]

obj = {'point': Point(1, 2)}
output = cjson.dumps(obj)
print(output)
```

输出结果：

```
{"point": [1, 2]}
```
