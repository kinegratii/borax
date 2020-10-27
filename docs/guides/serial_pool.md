# 序列号分配生成工具(Pool)

> 模块：`borax.counters.serial_pool`

> Add in v3.4.0

模块 `borax.counters.serial_pool` 。

## 使用示例

### 定义范围

`SerialNoPool` 支持以下方式的定义：



以下是几个常用的示例：

| 定义                                                        | value 范围 | label 范围              |
| ----------------------------------------------------------- | ---------- | ----------------------- |
| SerialNoPool(lower=0, upper=100)                            | 0 ~ 99     | -                       |
| SerialNoPool(base=10, digits=2)                             | 0 ~ 99     | -                       |
| SerialNoPool(label_fmt='LC{no:06d}')                        | 0 ~ 999999 | 'LC000000' ~ 'LC999999' |
| SerialNoPool(label_fmt='LC{no:04d}', lower=101, upper=1000) | 101 ~ 999  | 'LC101' ~ 'LC999'       |
| SerialNoPool(label_fmt='FF{no}', base=16, digits=2)         | 0 ~ 255    | 'FF00' ~ 'FFFF'         |
|                                                             |            |                         |
|                                                             |            |                         |

## 生成序列号



```python
from borax.counters.serial_pool import SerialNoPool

pool = SerialNoPool(label_fmt='FF{no}', base=16, digits=2)
data = pool.generate(num=2)
print(data) # ['FF00', 'FF01']

pool.add_elements(data)
data = pool.generate(num=2)
print(data) # ['FF02', 'FF03']
```



## API

### 序列号管理

- `SerialNoPool.add_elements(elements: ElementsType) -> 'SerialNoPool'`
- `SerialNoPool.remove_elements(elements: ElementsType) -> 'SerialNoPool'`
- `SerialNoPool.set_elements(elements: ElementsType) -> 'SerialNoPool'`

实现序列号池的增加、删除、重置。

- `SerialNoPool.set_source(source: Callable[[], ElementsType]) -> 'SerialNoPool'`

设置序列号池的回调函数，在此种方式下，SerialNoPool 内部不再保存具体的序列号集合。

### 生成函数

- `SerialNoPool.generate_values(num:int) -> List[int]`

生成 num 个的 序列值。

- `SerialNoPool.generate_labels(num:int) -> List[str]`

生成 num 个的 序列标签。