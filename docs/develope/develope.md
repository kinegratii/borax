# 技术文档

>  本节描述了Borax开源项目使用的技术思想、规范和工具。

## 开发特性和规范

本页是一个简要的工具清单，具体可以查看[《python项目持续集成与包发布》](https://kinegratii.github.io/2017/04/25/python-project-ci-publish/) 这篇文章。

### 类型提示 - Typing Hints

> PEP484: https://www.python.org/dev/peps/pep-0484/

类型提示是python3.5引入的功能。

### 代码风格 - Flake8

> Flake8工具：http://flake8.pycqa.org/en/latest/

### 测试框架 - nose2

> 主页：https://pypi.org/project/nose2/

### 持续构建 - Travis CI

> 主页： https://travis-ci.org



Travis是一个在线持续集成的平台，支持github登录。配置文件是一个名为 *.travis.yaml* 的配置文件。

### 发布 - twine

[twine](https://pypi.python.org/pypi/twine) 是一个专门用于发布项目到PyPI的工具，可以使用 `pip install twine` 来安装，它的主要优点：

- 安全的HTTPS传输
- 上传过程中不要求执行setup.py脚本
- 上传已经存在的文件，支持在发布前进行分发测试
- 支持任意包格式，包括wheel

### 项目徽章

在 [https://badge.fury.io](https://badge.fury.io/) 中输入项目名称并查找，把markdown格式复制到README.md文件。

点击Travis控制台build pass 图片并复制图片链接到README.md。



### 文档托管 - Docsify

> https://docsify.js.org
