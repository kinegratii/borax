# coding=utf8

import re
from decimal import Decimal

from typing import Union

RULES = [
    (r'零角零分$', '整'),
    (r'零[仟佰拾]', '零'),
    (r'零{2,}', '零'),
    (r'零([亿|万])', r'\g<1>'),
    (r'零+元', '元'),
    (r'亿零{0,3}万', '亿'),
    (r'^元', '零元')
]

MAX_VALUE_LIMIT = 1000000000000


def financial_amount_capital(num: Union[int, float, Decimal, str]) -> str:
    units = '仟佰拾亿仟佰拾万仟佰拾元角分'
    digits = '零壹贰叁肆伍陆柒捌玖'
    if isinstance(num, str):
        _n = int(num)
    else:
        _n = num
    if _n < 0 or _n >= MAX_VALUE_LIMIT:
        raise ValueError('Out of range')

    num_str = str(num) + '00'
    dot_pos = num_str.find('.')
    if dot_pos > -1:
        num_str = num_str[:dot_pos] + num_str[dot_pos + 1:dot_pos + 3]
    capital_str = ''.join([digits[int(i)] for i in num_str])
    s_units = units[len(units) - len(num_str):]

    o = ''.join('{}{}'.format(u, d) for u, d in zip(capital_str, s_units))
    for p, d in RULES:
        o = re.sub(p, d, o)

    return o
