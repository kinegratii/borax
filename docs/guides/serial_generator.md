# 序列号分配生成工具

> 模块：`borax.counters.serials`



## 背景

从整数范围分别生成若干个可用序列号。支持：

- 数字或字符串格式
- 多线程


## API

### generate_serials

函数签名

```python
def generate_serials(upper: int, num: int = 1, lower: int = 0, serials: Iterable[int] = None) -> List[int]:
    pass
```

参数：

- upper：整数范围的上限，不包含此数。
- lower：整数范围的下限，包含次数。
- num：分配ID的数量。
- serials：已经存在的ID，集合、列表类型。

如果无法生成，将抛出 `ValueError` 异常。

### SerialGenerator

ID分配生成器，可以在多次生成操作之间保存和维持ID数据。

例如：下面的例子从0到9生成3个序列号。

```python
sg = SerialGenerator(upper=10)
sg.add([0, 1, 2])
res = sg.generate(3) #  [3, 4, 5]
```

**generate**

`generate(self, num: int) -> List[int]`

返回若干个可用的序列号，内部调用 `generate_serials` 函数。

**add**

`add(self, elements: Iterable[int]) -> None`

添加若干个序列号。


**remove**

`remove(self, elements: Iterable[int]) -> None`

删除若干个序列号。



### StringSerialGenerator

基于字符串形式的序列号生成器。