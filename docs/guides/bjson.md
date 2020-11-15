# bjson 模块

> 模块：`borax.serialize.bjson`

> This module has been deprecated in v3.4.0 and will be removed in v4.0. 

## 使用方法

bjson 模块实现了一个自定义的 JSONEncoder ，支持通过 `__json__` 方法 encode 自定义对象。

例子：

```python
import json

from borax.serialize import bjson

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __json__(self):
        return [self.x, self.y]

obj = {'point': Point(1, 2)}
output = json.dumps(obj, cls=bjson.BJSONEncoder)
print(output)
```

输出结果：

```
{"point": [1, 2]}
```

bjson 还提供了类似的 `dumps` / `dump` 方法，默认使用 `BJSONEncoder` 。

例如：

```python
json.dumps(obj, cls=bjson.BJSONEncoder)
```

可以简化为：

```python
bjson.dumps(obj)
```



## API

- `borax.bjson.dumps(obj, **kwargs)` 
- `borax.bjson.dumps(obj, fp, **kwargs)` 

和 `json` 模块功能相同，使用 `BJSONEncoder` 编码器。