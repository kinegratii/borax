# 技术文档

本节描述了Borax开源项目使用的技术思想、规范和工具。本页是一个简要的工具清单，具体可以查看[《python项目持续集成与包发布》](https://kinegratii.github.io/2017/04/25/python-project-ci-publish/) 这篇文章。

## 开发基本SOP

1.  编写模块代码
1.  编写测试代码
1.  更新文档
1.  变更版本号
1.  执行单元测试： unittest / pytest
1.  代码静态检查 `flake8 borax tests`
1.  推送代码 commit信息： `:bookmark: release v3.4.0` ,emojj 意义参见 [gitmoji | git 提交信息的 emoji 指南](https://gitmoji.js.org/) 。
1.  检查确认 github action 的构建结果
1.  创建合并PR 标题    `Release v3.4.0 `
1.  创建 tag 和 release ，tag名称格式：`vx.y.z`
1.  构建wheel包
1.  上传到pypi，命令：`twine upload dist/borax-3.4.0-py2.py3.whl`
1.  同步到gitee仓库

## 编码实现

**关键字参数**

> PEP 3102: https://www.python.org/dev/peps/pep-3102/

对于一些函数参数必须使用关键字方式调用。

**类型提示 - Typing Hints**

> PEP484: https://www.python.org/dev/peps/pep-0484/

类型提示是python3.5引入的功能。

**代码风格 - Flake8**

> Flake8工具：http://flake8.pycqa.org/en/latest/

安装flake8

```shell
pip install flake8
```

运行代码检查

```shell
flake8 borax tests
```

## 单元测试

> 主页：https://docs.python.org/3/library/unittest.html

**测试框架**

从v3.3.1 开始，测试用例全部使用标准的 unittest 代码，支持 unittest / nose / nose2 / pytest 等测试框架。

**参数化测试**

参见 `unittest.TestCase.subTest` 。

**对象模拟**

参见 `unitest.mock` 。

## 持续集成

> 主页： https://github.com/kinegratii/borax/actions

Github Action 是 Github 推出的持续集成服务。包括以下内容：

- 单元测试
- 代码风格检查
- 代码覆盖率

## 版本发布

[twine](https://pypi.python.org/pypi/twine) 是一个专门用于发布项目到PyPI的工具，可以使用 `pip install twine` 来安装，它的主要优点：

- 安全的HTTPS传输
- 上传过程中不要求执行setup.py脚本
- 上传已经存在的文件，支持在发布前进行分发测试
- 支持任意包格式，包括wheel

## 文档


**文档托管 - Docsify**

> https://docsify.js.org

## 依赖库

参见  *requirements_dev.txt* 文档。