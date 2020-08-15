# coding=utf8

import decimal
import unittest

from borax.numbers import ChineseNumbers

decimal.getcontext().prec = 2


class ChineseNumberTestCase(unittest.TestCase):
    def test_chinese_number(self):
        self.assertEqual('一亿', ChineseNumbers.to_chinese_number(100000000))
        with self.assertRaises(ValueError):
            ChineseNumbers.to_chinese_number(-1)
