# coding=utf8

import unittest

from borax.numbers import ChineseNumbers


class ChineseNumberTestCase(unittest.TestCase):
    def test_chinese_number(self):
        self.assertEqual('一亿', ChineseNumbers.to_chinese_number(100000000))
        self.assertEqual('一千零四', ChineseNumbers.to_chinese_number(1004))
        self.assertEqual('二千零二十', ChineseNumbers.to_chinese_number(2020))
        self.assertEqual('十一', ChineseNumbers.measure_number(11))
        self.assertEqual('二十八', ChineseNumbers.measure_number('28'))
        with self.assertRaises(ValueError):
            ChineseNumbers.to_chinese_number(-1)

    def test_chinese_number_lower_order(self):
        self.assertEqual('二百〇四', ChineseNumbers.order_number(204))
        self.assertEqual('一千〇五十六', ChineseNumbers.order_number(1056))

    def test_chinese_number_upper_measure(self):
        self.assertEqual('贰佰零肆', ChineseNumbers.measure_number(204, True))
        self.assertEqual('贰佰零肆', ChineseNumbers.to_chinese_number(204, upper=True))

    def test_chinese_number_upper_order(self):
        self.assertEqual('贰佰〇肆', ChineseNumbers.order_number(204, upper=True))
        self.assertEqual('贰佰〇肆', ChineseNumbers.to_chinese_number(204, upper=True, order=True))
