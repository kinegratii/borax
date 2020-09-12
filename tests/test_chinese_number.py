# coding=utf8

import decimal
import unittest

from borax.numbers import ChineseNumbers

decimal.getcontext().prec = 2


class ChineseNumberTestCase(unittest.TestCase):
    def test_chinese_number(self):
        self.assertEqual('一亿', ChineseNumbers.to_chinese_number(100000000))
        self.assertEqual('十一', ChineseNumbers.measure_number(11))
        self.assertEqual('二十八', ChineseNumbers.measure_number('28'))
        with self.assertRaises(ValueError):
            ChineseNumbers.to_chinese_number(-1)

    def test_chinese_order_number(self):
        self.assertEqual('二百〇四', ChineseNumbers.order_number(204))
        self.assertEqual('一千〇五十六', ChineseNumbers.order_number(1056))
