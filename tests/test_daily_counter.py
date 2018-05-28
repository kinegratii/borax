# coding=utf8

import unittest

from borax.counters.daily import DailyCounter


class DailyCounterTestCase(unittest.TestCase):
    def test_init_instance(self):
        dc = DailyCounter(2015, 9)
        self.assertEqual(30, dc.days)
        self.assertEqual(2015, dc.year)
        self.assertEqual(9, dc.month)
        self.assertRaises(ValueError, dc.get_day_counter, 31)

    def test_init_instance_with_invalid_raw(self):
        self.assertRaises(ValueError, DailyCounter, 2015, 9, 'a,b,c')
        self.assertRaises(ValueError, DailyCounter, 2015, 9, '0,0,0')

    def test_increase(self):
        dc = DailyCounter(2015, 8)
        dc.increase(4, 2)
        self.assertTrue(2 == dc.get_day_counter(4))
