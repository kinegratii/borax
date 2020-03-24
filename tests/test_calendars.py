# coding=utf8


import unittest
from datetime import date

from borax.calendars.utils import get_last_day_of_this_month, get_fist_day_of_year_week


class LastDayTestCase(unittest.TestCase):
    def test_last_day(self):
        self.assertEqual(date(2019, 3, 31), get_last_day_of_this_month(2019, 3))
        self.assertEqual(date(2019, 2, 28), get_last_day_of_this_month(2019, 2))
        self.assertEqual(date(2020, 2, 29), get_last_day_of_this_month(2020, 2))

    def test_fist_day_of_week(self):
        self.assertEqual(date(2020, 2, 24), get_fist_day_of_year_week(2020, 9))
        self.assertEqual(date(2020, 1, 6), get_fist_day_of_year_week(2020, 1))
