import re
from decimal import Decimal

from typing import Union

__all__ = ['MAX_VALUE_LIMIT', 'LOWER_DIGITS', 'UPPER_DIGITS', 'ChineseNumbers', 'FinanceNumbers']

MAX_VALUE_LIMIT = 1000000000000  # 10^12

LOWER_UNITS = '千百十亿千百十万千百十_'
LOWER_DIGITS = '零一二三四五六七八九'

UPPER_UNITS = '仟佰拾亿仟佰拾万仟佰拾_'
UPPER_DIGITS = '零壹贰叁肆伍陆柒捌玖'


class ChineseNumbers:
    RULES = [
        (r'一十', '十'),
        (r'零[千百十]', '零'),
        (r'零{2,}', '零'),
        (r'零([亿|万])', r'\g<1>'),
        (r'亿零{0,3}万', '亿'),
        (r'零?_', ''),
    ]

    @staticmethod
    def measure_number(num: Union[int, str], upper: bool = False) -> str:
        """将数字转化为计量大/小写的中文数字，数字0的中文形式为“零”。

        >>> ChineseNumbers.measure_number(11)
        '十一'
        >>> ChineseNumbers.measure_number(204, True)
        '贰佰零肆'
        """
        if isinstance(num, str):
            _n = int(num)
        else:
            _n = num
        if _n < 0 or _n >= MAX_VALUE_LIMIT:
            raise ValueError('Out of range')
        num_str = str(num)
        capital_str = ''.join([LOWER_DIGITS[int(i)] for i in num_str])
        s_units = LOWER_UNITS[len(LOWER_UNITS) - len(num_str):]

        o = ''.join(f'{u}{d}' for u, d in zip(capital_str, s_units))
        for p, d in ChineseNumbers.RULES:
            o = re.sub(p, d, o)
        if 10 <= _n < 20:
            o.replace('一十', '十')
        if upper:
            for _ld, _ud in zip(LOWER_DIGITS + LOWER_UNITS[:3], UPPER_DIGITS + UPPER_UNITS[:3]):
                o = o.replace(_ld, _ud)
        return o

    @staticmethod
    def order_number(num: Union[int, str], upper: bool = False) -> str:
        """将数字转化为编号大/小写的中文数字，数字0的中文形式为“〇”。

        >>> ChineseNumbers.order_number(1056)
        '一千〇五十六'
        """
        val = ChineseNumbers.measure_number(num, upper)
        ns = val.replace('零', '〇')
        return ns

    @staticmethod
    def to_chinese_number(num: Union[int, str], upper: bool = False, order: bool = False) -> str:
        """

        >>> ChineseNumbers.to_chinese_number(100000000)
        '一亿'
        >>> ChineseNumbers.to_chinese_number(204, upper=True)
        '贰佰零肆'
        >>> ChineseNumbers.to_chinese_number(204, upper=True, order=True)
        '贰佰〇肆'
        """
        if order:
            return ChineseNumbers.order_number(num, upper)
        else:
            return ChineseNumbers.measure_number(num, upper)


class FinanceNumbers:
    RULES = [
        (r'零角零分$', '整'),
        (r'零[仟佰拾]', '零'),
        (r'零{2,}', '零'),
        (r'零([亿|万])', r'\g<1>'),
        (r'零+元', '元'),
        (r'亿零{0,3}万', '亿'),
        (r'^元', '零元')
    ]

    @staticmethod
    def to_capital_str(num: Union[int, float, Decimal, str]) -> str:
        """Convert a int or float object to finance numeric string.

        >>> FinanceNumbers.to_capital_str(100000000)
        '壹亿元整'
        >>> FinanceNumbers.to_capital_str(80.02)
        '捌拾元零角贰分'
        >>> import decimal
        >>> FinanceNumbers.to_capital_str(decimal.Decimal(4.50))
        '肆元伍角零分'
        """
        units = UPPER_UNITS[:-1] + '元角分'
        if isinstance(num, str):
            _n = Decimal(num)
        else:
            _n = num
        if _n < 0 or _n >= MAX_VALUE_LIMIT:
            raise ValueError('Out of range')

        num_str = str(num) + '00'
        dot_pos = num_str.find('.')
        if dot_pos > -1:
            num_str = num_str[:dot_pos] + num_str[dot_pos + 1:dot_pos + 3]
        capital_str = ''.join([UPPER_DIGITS[int(i)] for i in num_str])
        s_units = units[len(units) - len(num_str):]

        o = ''.join(f'{u}{d}' for u, d in zip(capital_str, s_units))
        for p, d in FinanceNumbers.RULES:
            o = re.sub(p, d, o)

        return o
