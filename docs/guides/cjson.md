# cjson 模块

> 模块：`borax.serialize.cjson`

## v3.4更新

自v3.4.0 开始:

1. 原来的 `bjson` 和 `cjson` 将合并为 `cjson`，`cjson` 现在也支持 `__json__` 定义。
2. 编码函数 `cjson.to_serializable` 将重名为 `cjson.encoder`。
3. `bjson` 模块 和 `cjson.to_serializable` 函数别名将在v4.0版本移除。

## 使用方法

### 基础原理

在使用 `json.dump/json.dumps` 序列化 Python 对象时，对于无法序列化的类型，用户必须实现自己的序列化逻辑（如 `json.JSONEncoder`），这就是参数 `default` （基于函数）和 `cls` （基于类）的作用。

`cjson.encoder` 实现了一个基于函数的 `json.JSONEncoder` ，用于 `default` 参数。

```python
import json
from borax.serialize import cjson

json.dumps([1, 2, 3], default=cjson.encoder)
```

`cjson.encoder` 支持两种方式的序列化逻辑定义。

### 分开定义

即 在 *需要序列化的自定义类* 一侧使用 `__json__` 方法定义。

例子：

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __json__(self):
        return [self.x, self.y]
```

### 集中定义

即 在 *cjson模块* 一侧使用 `cjson.encoder.register` 装饰器定义。 例子：

```python
from borax.serialize import cjson

class EPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@cjson.encoder.register(EPoint)
def encode_epoint(o):
    return [o.x, o.y]
```

`encoder.register` 是一个标准的装饰器，上述也可以使用下面的简便形式：

```
cjson.encoder.register(EPoint, lambda o: [o.x, o.y])
```

### 调用和序列化

使用 `cjson.dumps` 即可。

```python
from borax.serialize import cjson

p1 = Point(1, 2)
p2 = EPoint(1, 2)

output1 = cjson.dumps({'point1':p1, 'point2':p2}) # 输出 {"point1": [1, 2], "point2": [1, 2]}
```

该函数按照下列方式执行序列化逻辑 ：

1. 调用 `encoder`，如果抛出 `TypeError` 将忽略这种方式。
2. `__json__` 

即，对于具有两种定义方式的同一个类型， *集中定义* 方式将优先于 *分开定义* 方式。

```python
from borax.serialize import cjson

class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __json__(self):
        return [self.x, self.y]

@cjson.encoder.register(Pt)
def encode_pt(p):
    return {'x': p.x, 'y': p.y}

obj = {'point': Pt(1, 2)}
print(cjson.dumps(obj)) # 输出：'{"point": {"x": 1, "y": 2}}'

cjson.encoder.register(Pt, cjson.encode_object)

obj = {'point': Pt(1, 2)}
print(cjson.dumps(obj)) # 输出：'{"point": [1, 2]}'
```

### encoder进阶: dispatch容器

对于上层调用者  `json`  来说， `cjson.encoder` 和 `cjson.to_serializable` 是一样的，都是 callable 。

但是在内部实现上，`cjson.encoder` 更像是一个 Mapping 容器，由 `{类对象: callable }` 组成。这也是我们使用 *名词* 命名该函数的重要原因。

- 只能使用 `register`  方法添加新的映射实现，且没有 unregister / delete 等方法（参考 [这里](https://stackoverflow.com/a/25951784)）
- 内部使用 `weakref.WeakKeyDictionary` 组织，可以认为是一个简单的分组。

## API

### cjson.encode_object

cjson 默认的编码函数。调用 `__json__` 进行编码。

### cjson.encoder

使用 [singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch) 装饰的json encoder函数，可以直接用于 dump 的 default 参数。

使用 `register` 重载新的编码实现， 默认添加了对 `datetime` 、`date` 的序列化支持。

```python
encoder.register(datetime, lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S'))
encoder.register(date, lambda obj: obj.strftime('%Y-%m-%d'))
```

### cjson.CJSONEncoder

> Add in v3.5.3

可用于 `json.dump` 函数cls参数。

### cjson.dumps/dump

cjson 还提供了类似的 `dumps` / `dump` 方法，默认使用 `cjson.encoder` 函数。

- `borax.serialize.cjson.dumps(obj, **kwargs)` 
- `borax.serialize.cjson.dumps(obj, fp, **kwargs)` 

下面两个语句是等效的。

```
json.dump(obj, default=cjson.encoder)

json.dump(obj, cls=cjson.CJSONEncoder)

cjson.dump(obj)
```

## 参考资料

- [PEP 443 -- Single-dispatch generic functions](https://www.python.org/dev/peps/pep-0443/)