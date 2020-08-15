# tree 模块

> 模块： `borax.structure.tree`

> Added in V1.1.4

## 功能

`tree.pll2cnl` 能够将易于存储的 *Parent线性数组* 转化为 *Children嵌套数组* 形式。


Parent线性数组(ParentLinearList)格式：
```json
[
    {"id": 1, "name": "node1", "parent": null},
    {"id": 2, "name": "child1", "parent": 1},
    {"id": 3, "name": "child2", "parent": 1},
    {"id": 4, "name": "node2", "parent": null},
    {"id": 5, "name": "child3", "parent": 5}
]
```


Children嵌套数组(ChildrenNestedList) 格式：

```json
[
    {
        "name": "node1", "id": 1,
        "children": [
            { "name": "child1", "id": 2 },
            { "name": "child2", "id": 3 }
        ]
    },
    {
        "name": "node2", "id": 4,
        "children": [
            { "name": "child3", "id": 5 }
        ]
    }
]
```

## 应用场景

可作为相关插件的远程数据构建工具，包括：

- [jqTree](http://mbraak.github.io/jqTree/)
- [jsTree](https://www.jstree.com/)
- [ECharts 旭日图/矩形树图/树图](http://echarts.baidu.com/)

## API

该模块只有一个函数 pll2cnl ，函数签名


```python
def pll2cnl(
        nodelist,
        *,
        id_field='id',
        parent_field='parent',
        root_value=None,
        children_field='children',
        flat_fields=None,
        extra_fields=None,
        extra_key=None

):
    pass
```

> pll2cnl 的全称为 parent-linear-list-to-children-nested-list 。

参数定义如下：

| 属性 | 类型 | 描述 | 其他 |
| ------ | ------ | ------ | ------ |
| id_field | `str` | 主键字段名称  | |
| parent_field | `str` | 父节点字段名称 | |
| root_value | `Any` | 根节点的主键值 | 通常取值 `None`、`-1` 等 |
| children_field | `str` | 子节点字段名称 | |
| flat_fields | `list` | 同级字段列表 | |
| extra_key | `str` | 额外数据的键名称 | |
| extra_fields | `list` | 其他字段列表 | |

其他参数要求：

- `id_field`，`children_field`, `extra_key`, `flat_fields` 必须选取不同的值。

一个节点的通用格式如下：

```
{
    <id_field>: <id_field_value>,
    <extra_key>:{
        <e_k1>: <e_v1>,
        <e_k2>: <e_v2>,
        ...
    }
    <f_k1>:<f_v1>,
    <f_k2>:<f_v2>,
    ...
    <children_field>:[
        <Node>,
        ...
    ]
}
```

例如对于配置 `{"extra_key": "extra", extra_fields":"name"}` ，上述节点将输出为以下格式：

```json
{
    "id": 0,
    "extra":{
        "name":"A"
    }
}
```

