import decimal
import unittest

from borax.numbers import FinanceNumbers

decimal.getcontext().prec = 2


class CapitalNumber(unittest.TestCase):
    def test_amount_capital(self):
        self.assertEqual('壹亿元整', FinanceNumbers.to_capital_str(100000000))
        self.assertEqual('肆佰伍拾柒万捌仟肆佰肆拾贰元贰角叁分', FinanceNumbers.to_capital_str(4578442.23))
        self.assertEqual('贰佰叁拾肆元整', FinanceNumbers.to_capital_str(234))
        self.assertEqual('捌拾元零角贰分', FinanceNumbers.to_capital_str(80.02))

    def test_decimal(self):
        self.assertEqual('肆元伍角零分', FinanceNumbers.to_capital_str(decimal.Decimal(4.50)))
        self.assertEqual('壹拾万柒仟元伍角叁分', FinanceNumbers.to_capital_str(decimal.Decimal('107000.53')))
        self.assertEqual('壹拾万柒仟元伍角叁分', FinanceNumbers.to_capital_str('107000.53'))

    def test_valid_range(self):
        with self.assertRaises(ValueError):
            FinanceNumbers.to_capital_str(332342342341234)
        with self.assertRaises(ValueError):
            FinanceNumbers.to_capital_str(1000000000000)
        self.assertIsNotNone(FinanceNumbers.to_capital_str(999999999999))
        self.assertIsNotNone(FinanceNumbers.to_capital_str(999999999999.99))
        with self.assertRaises(ValueError):
            FinanceNumbers.to_capital_str('1000000000000')
