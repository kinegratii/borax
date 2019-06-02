# 更新日志

## v1.4.2

- `counters.serials` 模块
  - `StringSerialGenerator` 支持2/8/10/16进制格式
  
## v1.4.1 (20190602)

- `borax.system` 模块
  - 新增 `rotate_filename` 文件名转换函数
- `counters.serials` 模块
  - 修正 `generate_serials` 异常提示错误

## v1.4.0 (20190519)

> 本版本调整了若干个模块组织结构。

- `counters.serials` 模块
  - 新增序列号生成器 `SerialGenerator`
- `borax-cli` 命令行工具
  - 新增 `mpi` 命令
- `borax.strings` 模块
  - 新增 `camel2snake`、`snake2camel` 方法
- `borax.htmls` 模块
  - 新增 `HTMLString` 类
  - 新增 `html_tag` 生成器
- `borax.system` 模块
  - 新增检查可执行文件 `check_path_variables`
  - `borax.loader.load_class` 移至本模块
- `borax.decorators.admin` 模块
  - 废弃本模块

## v1.3.1 (20190416)

- `fetch` 模块
  - 新增 `fetch_as_dict` 函数
  - 新增 `bget` 接口

## v1.3.0 (20190309)

- `calendars.lunardate` 模块
  - 重新修订农历信息，通过微软数据源的验证
  - 新增 `weekday` 和 `isoweekday` 方法
  - 补充公历2101年日期的干支、节气信息
  - 修正无节气的日期格式化的bug
  - 新增 sqlte3 自定义字段支持
  - 新增 `%F` 字符串描述符
- `calendars.festivals` 模块
  - 新增 `encode` / `decode` 方法，支持序列化
  - 新增 `FestivalFactory` ，支持节日分组分类
  - 支持省略年份的字符表达式
  - 修正 `SolarSchema` 二月倒数序号形式解析的bug
- `calendars.birthday` 模块
  - 新增虚岁/周岁的计算函数
- 新增 `borax.structures.proxy` 模块
- `trim_iterable` 新增前缀、后缀字符串

## v1.2.0 (20190213)

> 部分模块新增 [Typing Hint](https://docs.python.org/3/library/typing.html) 支持

- `calendars.festivals` 模块
  - 支持节日查找
- `calendars.lunardate` 模块
  - 使用新版节气数据存储方式
  - 新增 `LCalendars` 工具接口
  - 新增`%A`、`%B` 字符串描述符
- 新增 travis 构建
  
## v1.1.9 (20190113)

- `choices` 模块
  - 修正`Item.default` 未设置的bug

## v1.1.8 (20190108)

- `calendar` 模块
  - 新增获取昨日/明日日期的方法
  - 新增 `replace` 函数
  - 新增格式化函数 `strftime`
- `lookup` 模块
  - 新增 `select_as_dict` 方法，废弃 `data_dict` 方法
- `loader` 模块
  - 新增 `load_class` 类加载器
  
## v1.1.7 (20190102)

- `calendar` 模块
  - 新增 `from borax.calendar import LunarDate` 快捷导入路径
- `lookup` 模块
  - 新增 `data_dict` 方法

## v1.1.6 (20181112)

- 新增 `TableLookup` 模块 `borax.structures.lookup`
- `choices` 模块
  - `choices.ConstChoices` 支持类继承
  - `choices.Item` 支持自定义 order 排序
- `lookup` 模块
  - `TableLookup` 支持列表迭代特性

## v1.1.5 (20180923)

- 新增 tkinter 异步模块 `borax.ui.aiotk`
- 新增 tkinter 控件模块 `borax.ui.widgets`

## v1.1.4 (20180916)

- 新增树形数据模块 `borax.structure.tree`
- 新增 json 自定义Encoder模块 `borax.serialize.cjson`

## v1.1.3 (20180902)

- 新增财务金额大写工具 `borax.finance`
- 新增自定义 JSON 序列化协议

## v1.1.2 (20180819)

- 新增农历日期工具模块 `borax.calendars.lunardate`

## v1.1.1 (20180804)

- 适配 Python3.7
- 新增 `borax.decorators.admin` 模块

## v1.1.0 (20180525)

- 新增百分比类 `Percentage`
- 发布在线文档

## v1.0.3 (20180504)

- 新增单例设计模式实现
- `borax.lazy` 移到 `borax.patterns.lazy`

## v1.0.2 (20180418)

- 修正发布配置文件

## v1.0.1 (20180411)

- 新增 `structure.daily.DailyCounter` 月份统计类
- `lazy` 模块
  - `LazyObject` 初始化函数支持 `args` 和 `kwargs` 参数

## v1.0.0 (20180328)

- 发布第一个版本