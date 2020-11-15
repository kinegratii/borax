# coding=utf8


import re
from decimal import Decimal

from typing import Union

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
    def measure_number(num: Union[int, str]) -> str:
        if isinstance(num, str):
            _n = int(num)
        else:
            _n = num
        if _n < 0 or _n >= MAX_VALUE_LIMIT:
            raise ValueError('Out of range')
        num_str = str(num)
        capital_str = ''.join([LOWER_DIGITS[int(i)] for i in num_str])
        s_units = LOWER_UNITS[len(LOWER_UNITS) - len(num_str):]

        o = ''.join('{}{}'.format(u, d) for u, d in zip(capital_str, s_units))
        for p, d in ChineseNumbers.RULES:
            o = re.sub(p, d, o)
        if 10 <= _n < 20:
            o.replace('一十', '十')
        return o

    @staticmethod
    def order_number(num: Union[int, str]) -> str:
        val = ChineseNumbers.measure_number(num)
        return val.replace('零', '〇')

    @staticmethod
    def to_chinese_number(num: Union[int, str], upper: bool = False, order: bool = False) -> str:
        if order:
            lower_string = ChineseNumbers.order_number(num)
        else:
            lower_string = ChineseNumbers.measure_number(num)
        if upper:
            for _ld, _ud in zip(LOWER_DIGITS + LOWER_UNITS[:3], UPPER_DIGITS + UPPER_UNITS[:3]):
                lower_string = lower_string.replace(_ld, _ud)
        return lower_string


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

        o = ''.join('{}{}'.format(u, d) for u, d in zip(capital_str, s_units))
        for p, d in FinanceNumbers.RULES:
            o = re.sub(p, d, o)

        return o
