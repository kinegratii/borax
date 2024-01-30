# 开发笔记

## python版本约束

Borax 4.1.0开始，要求python最低版本为3.9，主要是引入了新的特性，包括：

- `functools.cached_property` 装饰器 (python3.8+)
- `typing.Literal` 类型注释(python3.8+)

## 代码风格

项目代码风格以 [PEP8](https://peps.python.org/pep-0008/) + pycharm 的配置为基准，并增加下列的一些自定义规则。

- 代码每行长度限制为120
- 函数复杂度限制为25
- 禁止使用 `\` 作为代码行分割的标志，需使用括号
- 不再接受注释方式的类型声明，如 `a = 2 # type:int` 应该为 `a:int = 2` (pyflake触发 `F401` 警告)

## 项目开发

Borax 默认使用 *pyproject.toml* 文件作为项目配置文件，具体包括单元测试、静态检查等内容。

*pyproject.toml* 配置文件目前包括以下内容：

| 功能         | 开发库   | 独立配置文件 | pyproject.toml配置段 | 备注                       |
| ------------ | -------- | ------------ | -------------------- | -------------------------- |
| 项目基本信息 | -        |              | [project]            |                            |
| 单元测试     | nose2    |              |                      |                            |
| 覆盖率       | coverage |              | [tool.coverage]      |                            |
| 静态检查     | flake8   |              | [tool.flake8]        | 通过 Flake8-pyproject 实现 |
| 静态检查     | pylint   | .pylintrc    |                      | 配置项过多，不进行迁移     |
| 项目构建     | build    |              | [tool.setuptool]     |                            |



## 项目构建

项目使用 `build` 作为包构建工具，使用下列命令生成 wheel 文件。

```shell
python -m build -w
```

## 文档编写

除了常规的模块文档外，项目包括以下两种日志文档：

- 更新日志：每个版本的changelog。
- 发布日志：某些重要版本的 release note，每个版本单独一篇文章。

## 文档生成

Borax项目使用 [Material for MkDocs ](https://squidfunk.github.io/mkdocs-material/)  作为文档生成工具，不再支持 docsify 文档生成工具。
