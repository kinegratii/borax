# 技术文档

本节描述了Borax开源项目使用的技术思想、规范和工具。本页是一个简要的工具清单，具体可以查看[《python项目持续集成与包发布》](https://kinegratii.github.io/2017/04/25/python-project-ci-publish/) 这篇文章。

## 编码

**类型提示 - Typing Hints**

> PEP484: https://www.python.org/dev/peps/pep-0484/

类型提示是python3.5引入的功能。

**代码风格 - Flake8**

> Flake8工具：http://flake8.pycqa.org/en/latest/

## 持续集成

**测试框架**

> 主页：https://pypi.org/project/nose2/

从v3.3.1 开始，测试用例全部使用标准的 unittest 代码，支持 unittest / nose / nose2 / pytest 等测试框架。

**持续构建 - Github Action**

> 主页： https://github.com/kinegratii/borax/actions

Github Action 是 Github 推出的持续集成服务。

**发布 - twine**

[twine](https://pypi.python.org/pypi/twine) 是一个专门用于发布项目到PyPI的工具，可以使用 `pip install twine` 来安装，它的主要优点：

- 安全的HTTPS传输
- 上传过程中不要求执行setup.py脚本
- 上传已经存在的文件，支持在发布前进行分发测试
- 支持任意包格式，包括wheel

## 文档

**项目徽章**

在 [https://badge.fury.io](https://badge.fury.io/) 中输入项目名称并查找，把markdown格式复制到README.md文件。

点击Travis控制台build pass 图片并复制图片链接到README.md。


**文档托管 - Docsify**

> https://docsify.js.org

## 依赖库

Borax开发依赖库的版本如下：

```
nose2~=0.9
coverage~=5.2
flake8~=3.8
mccabe~=0.6
wheel~=0.35
setuptools~=47.3
```

