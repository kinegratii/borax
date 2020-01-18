# V3.0.0发布日志

## 概述

2019年11月15日，Borax 正式发布 V3.0.0 。

## 1 Borax-Cli

Borax-V3 新增一系列命令行工具。

### windows/unix文件换行符转化

转换为 Unix 风格的换行符

```shell
// 转换单个文件
$ borax-cli w2u install.sh

//转化多个文件，并输出到另外一个目录
$ borax-cli w2u *.sh --output dist/scripts
```