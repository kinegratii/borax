# coding=utf8

import decimal
import unittest

from borax.finance import financial_amount_capital

decimal.getcontext().prec = 2


class CapitalNumber(unittest.TestCase):
    def test_amount_capital(self):
        self.assertEqual('壹亿元整', financial_amount_capital(100000000))
        self.assertEqual('肆佰伍拾柒万捌仟肆佰肆拾贰元贰角叁分', financial_amount_capital(4578442.23))
        self.assertEqual('贰佰叁拾肆元整', financial_amount_capital(234))
        self.assertEqual('捌拾元零角贰分', financial_amount_capital(80.02))

    def test_decimal(self):
        self.assertEqual('肆元伍角零分', financial_amount_capital(decimal.Decimal(4.50)))
        self.assertEqual('壹拾万柒仟元伍角叁分', financial_amount_capital(decimal.Decimal('107000.53')))
