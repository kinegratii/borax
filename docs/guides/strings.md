# 字符串工具

> 模块 borax.strings

本模块提供了一系列有关字符串处理的工具函数。

## 命名风格



- `camel2snake(s: str) -> str`

将罗马尼亚风格转化为驼峰命名法

- `snake2camel(s: str) -> str`

将驼峰命名法转化为罗马尼亚风格

## 文件换行符

在不同的操作系统，文件换行符使用不同的字符表示。

| 操作系统 | 换行符 |
| -------- | ------ |
| Windows  | \r\n   |
| Linux    | \n     |

`borax.strings.FileEndingUtil` 提供了处理不同换行符的转换函数。

- `FileEndingUtil.windows2linux(content: bytes) -> bytes`
- `FileEndingUtil.linux2windows(content: bytes) -> bytes`

将 content 中的换行符进行转化。content 必须是 bytes 类型。