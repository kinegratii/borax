# 更新日志

## v4.1.1

- 新增创建农历年或农历月最后一天的方法 `LunarDate.last_day`
- `SolarFestival` 和`LunarFestival` 初始化函数 `freq` 参数支持字符串设置（ [ #56](https://github.com/kinegratii/borax/issues/56) ）
- `Period.solar_year` 和 `Period.lunar_year` 新增 `end_year` 参数，支持跨年份计算
- 废弃模块：`borax.choices`

## v4.1.0 (20240131)

> Borax最低python版本要求为python3.9

[发布日志](/release-note/v410)

- 功能更新
  - 新增 [Borax日历应用](/guides/borax_calendar_app) 
  - 包 `borax.apps` 变更为 `borax.capp`
  - 新增方法 `FestivalLibrary.extend_term_festivals` 
  - 新增方法 `FestivalLibrary.load`
  - 新增 `borax.ui.widgets.MessageLabel` 类
  - `Festival` 类新增 `code` 属性
  - `WrappedDate.solar` 和 `WrappedDate.lunar` 属性变更为只读属性，不可写入
- 项目构建
  - 不再支持python3.7和python3.8
  - 本地开发环境更新至 python3.11.7
  - 使用 *pyproject.toml* 项目构建配置文件，构建命令 `python -m build -w`
  - 支持python3.12
- 项目文档
  - mkdocs-material 更新至 9.5.3
  - 不再支持 docsify 构建（index.html 冲突）

## v4.0.0 (20221115)

[发布日志](/release-note/v400)

- 新增基于 tkinter 的 [节日界面库](/guides/festivals2-ui)
- 移除源代码文件编码声明行
- 移除 `borax.calendars.festival` 模块
- 修正 `LunarDate` 显示星期错误的问题 （[#49](https://github.com/kinegratii/borax/issues/49)）
- `FestivalLibrary.list_days_in_countdown` 新增 `countdown_ordered` 参数，表示是否按倒计天数排序
- `FestivalLibrary.load_builtin` 支持创建空库
- `FestivalLibrary` 新增删除元素函数 `delete_by_indexes`

## v3.5.6 (20220703)

[发布日志](/release-note/v356)

- 新增Docs Test
- `borax.calendars.lunardate`
  - 新增文本解析函数 `LunarDate.strptime` （[#44](https://github.com/kinegratii/borax/issues/44)）
  - 新增格式化修饰符 `%c`
  - 新增 `TextUtils.gz2offset` / `TextUtils.offset2gz` 干支转化方法
- `borax.calendars.festivals2`
  - 星期型节日支持倒数序号 和 每月频率（[#43](https://github.com/kinegratii/borax/issues/43)）
  - "除夕"节日修改为“农历年最后一天”而不是“十二月最后一天”
  - 修正三伏九九天计算错误的BUG（[#45](https://github.com/kinegratii/borax/issues/45)）
  - `TermFestival` 支持干支日推算的节日 （[#46](https://github.com/kinegratii/borax/issues/46)）
  - `TermFestival` 新增 term 参数
  - 节气名称支持拼音首字母形式
- `borax.structures.percentage`
  - 优化底层百分数格式化显示 
- `borax.devtools`
  - 新增 `RuntimeMeasurer.print_` 方法

## v3.5.5 (20220504)

- `borax.calendars.festivals2`
  - `FestivalLibrary.iter_month_daytuples` 新增 `return_pos` 参数，可返回日期位置
  - `Festival` 新增 `list_days_in_future` / `list_days_in_past` 函数
- `borax.calendars.utils`
  - 修正 `ThreeNineUtils` 内部计算错误的BUG
- `borax.htmls`
  - `html_tag` 函数新增 width / height 参数
  - 修正 `html_tag` 函数style参数解析空值的BUG

## v3.5.4 (20220314)

- `borax.htmls`
  - `html_tag` 函数css参数支持str类型（函数逻辑已支持，本次仅添加typing hints）
- `borax.datasets.fetch` 模块
  - 修正 `fetch` 解析错误的bug （[#39](https://github.com/kinegratii/borax/issues/39)）

## v3.5.3 (20220303)

- `borax.serialize.cjson`
  - 新增用于`json.dump`函数cls参数的 `CJSONEncoder` 类
- `borax.datasets.fetch` 模块
  - 修正 `fetch` 解析列表型数据错误的bug （[#39](https://github.com/kinegratii/borax/issues/39)）
- `borax.system` 模块
  - 新增 `load_class` 的别名函数 `load_object`

## v3.5.2 (20220118)

- `borax.calendars.lunardate`
  - 新增 `TermUtils.nth_term_day` 获取节气日期函数
- `borax.calendars.festivals2`
  - Festival新增str/repr方法
  - `FestivalLibrary`新增日历月相关函数 iter_month_daytuples/monthdaycalendar
- `borax.htmls`
  - `html_tag` 函数支持style/css参数解析

## v3.5.1 (20220101)

- `borax.calendars.lunardate`
  - `LunarDate.strftime` 新增 `%W` 中文星期格式化
  - 修改 `%F` 在“闰月/冬月/腊月”情况下表述为“闰X月/十一月/十二月”
- `borax.calendars.festivals2`
  - 新增 `Festival.gets` 获取属性方法
  - 新增 `Festival.description` 属性，表示规范化中文描述
  - 新增 `FestivalLibrary.extend_unique` ，支持以去重方式添加新节日
- `borax.calendars.utils`
  - 新增 `ThreeNineUtils` 三伏九九天解析工具
- `borax.numbers`
  - measure_number/order_number新增upper参数
- 开发SOP
  - 移除whl安装包文件的py2标识 

## v3.5.0 (20211115)

> 新增 Python3.10构建支持

- `borax.calendars.lunardate`
  - 移除 `LCalendars.is_leap_month` 函数
- `borax.calendars.festivals2`
  - 全新的节日库模块 `festivals2`
  - `festivals` 标记为废弃，将在v3.6移除
- `borax.serialize`
  - 移除 `bjson` 模块
  - 移除 `cjson.to_serializable` 函数
- `borax.datasets.join_`模块
  - 移除 `old_join` 和 `old_join_one` 函数
- 移除 `borax.finance` 模块
- 开发SOP
  - 更新依赖库，参见 *requirements_dev.txt*

## v3.4.4 (20210410)

- `borax.calendars.lunarDate`
  - 修正 `LCalendars.create_solar_date` 在2101年份无法创建的BUG（[#28](https://github.com/kinegratii/borax/issues/28)）

## v3.4.3 (20210201)

- `borax.calendars.lunarDate`
  - `LunarDate.leap` 使用 `int` 类型 （[#26](https://github.com/kinegratii/borax/issues/26)）

## v3.4.2  (20201227)

- `borax.datasets.join`
  - `join` 新增 defaults 参数

## v3.4.1  (20201125)

- **`borax.calendars.lunarDate`**
  - 修正农历日中文名称 `LunarDate.cn_day` 二十、三十日表示错误的BUG （[#22](https://github.com/kinegratii/borax/issues/22)）
  - 修正日历日名称 `LunarDate.cn_day_calendar` 表示错误的BUG（[#20](https://github.com/kinegratii/borax/issues/20)）
- **`borax.htmls`**
  - 移除html自闭合标签不必要的斜杠字符

## v3.4.0 (20201115)

> 新增 Python3.9构建支持

- **`borax.choices`**
  - `ConstChoices` 新增 labels 、values 等属性
- **`borax.calendars.lunarDate`**
  - 新增 `%N` 月份描述符，将“冬”、“腊”显示为“十一”、“十二”
  - 新增 `LCalendars.get_leap_years` 函数
  - 新增 `InvalidLunarDateError` 异常类
  - 修正农历平月日期 `%t` 格式化显示的BUG
- `borax.datasets.join`
  - 新增 `deep_join` 、`deep_join_one` 使用赋值传参方式
- **`borax.numbers`**
  - `ChineseNumbers` 类新增 计量/编号 两种数字形式
- **`borax.htmls`**
  - 修正函数 `html_tag` 处理的BUG
- **`borax.serialize`**
  - 整合 `bjson` 和 `cjson` ，`cjson` 支持 `__json__` 特性
  - 模块 `bjson` 标记为 `DeprecationWarning` 状态
- **开发SOP**
  - 支持 [Github Action](https://github.com/kinegratii/borax/actions) 
  - 更新依赖库，参见 *requirements_dev.txt*
  - 新增代码覆盖率 [Codecov](https://codecov.io/)

## v3.3.1 (20200827)

- `borax.structures.dictionary` 模块
  - 类 `AttrDict` 新增别名 `AD`
- 开发SOP
  - 修正因stacklevel 设置错误导致 `DeprecatedWarning` 无法正确提示的BUG
  - 参数化测试改用 `unittest.TestCase.subTest`
  - 支持 unittest / nose / nose2 / pytest 测试框架
  - 重新组织Borax文档

## v3.3.0 (20200815)

- `borax.datasets.join_` 模块
  - `old_join` 和 `old_join_one` 标记为 PendingDeprecationWarning  ，将在 v3.5移除
- `borax.runtime` 模块
- `borax.numbers` 模块 (+)
  - 新增 `ChineseNumbers` 类
  - 新增 `finaceNumbers` 类，由 `borax.finace` 模块转化
- `borax.finance` 模块
  - 修正小数使用字符串时 `financial_amount_capital` 错误的BUG
  - 本模块被标记为 `PendingDeprecationWarning` 
- 被移除模块
  - `borax.structures.dic`
  - `borax.fetch` 

## v3.2.0 (20200510)

> 本版本重写 `borax.datasets.join_` 模块，接口引入重大变更，详情查看 [join模块](guides/join) 。

- `borax.datasets.join_`模块
  - 重写 `join` 和 `join_one` 函数，原有的重命名为 `old_join` 和 `old_join_one`
  - 原有的 `old_*` 将在v4.0版本移除。
- 新增 `borax.calendars.utils` 模块
- `borax.structures.percentage` 模块
  - 新增 `format_percentage` 函数
  - 类 `Percentage` 新增 `fraction_display` 属性
  - 当 total 为 0 ，显示为 `'-'` ，而不是 `'0.00%'`
- `borax.fetch` 模块
  - 本模块被标记为 DeprecationWarning ，将在v3.3移除

## v3.1.0 (20200118)

> 新增 Python3.8构建支持

- `datasets` 包
  - 新增 `borax.datasets.fetch`
  - 新增 `borax.datasets.join_` 模块
  - `join_one` 新增 default 参数
- `calendars.lunardate` 模块
  - 修正农历闰月转平月错误的BUG ([#11](https://github.com/kinegratii/borax/issues/11))
- `borax.fetch` 模块
  - 本模块被标记为 PendingDeprecationWarning ，将在v3.3移除

## v3.0.0 (20191125)

- `borax.strings` 模块
  - 新增 windows/linux 换行符转换 `FileEndingUtils`
- `borax.structures` 模块
  - 移除 `TableLookup.data_dict`  方法
- `borax.counters.serials` 模块
  - 新增 `SerialGenerator.generate_next_one` 方法
- `borax.finance` 模块
  - `financial_amount_capital` 新增上下限检查
- 移除 `borax.loader`
- 移除 `borax.decorators.admin`

## v1.4.2 (20190717)

- `counters.serials` 模块
  - `StringSerialGenerator` 支持2/8/10/16进制格式
- `borax.decorators.admin` 模块
  - 修复默认值的bug

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
  - 新增 sqlite3 自定义字段支持
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