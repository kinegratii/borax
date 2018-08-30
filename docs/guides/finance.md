# Finance 模块

> 模块：`borax.finance`

finance 提供了一系列的此物财务金融工具。

## 大写金额

将数字转化为财务大写金额的字符串，函数签名：

```
financial_amount_capital(num:[number,str, Decimal]) -> str
```

输入值可以为以下几种类型：

- 数字：如 `32`, `4.56` 等；
- 字符串，如 `'32'`, `'4.56'` 等；
- 小数，如 `decimal.Decimal('8.29')` 等。

例子：

```
>>> from borax.finance import financial_amount_capital
>>> financial_amount_capital(100000000)
'壹亿元整'
>>>financial_amount_capital(4578442.23)
'肆佰伍拾柒万捌仟肆佰肆拾贰元贰角叁分'
>>>financial_amount_capital(107000.53)
壹拾万柒仟元伍角叁分
```