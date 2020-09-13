# coding=utf8


import unittest
from datetime import date

from borax.calendars.utils import SCalendars


class LastDayTestCase(unittest.TestCase):
    def test_last_day(self):
        self.assertEqual(date(2019, 3, 31), SCalendars.get_last_day_of_this_month(2019, 3))
        self.assertEqual(date(2019, 2, 28), SCalendars.get_last_day_of_this_month(2019, 2))
        self.assertEqual(date(2020, 2, 29), SCalendars.get_last_day_of_this_month(2020, 2))

    def test_fist_day_of_week(self):
        self.assertEqual(date(2020, 2, 24), SCalendars.get_fist_day_of_year_week(2020, 8))
        self.assertEqual(date(2020, 1, 6), SCalendars.get_fist_day_of_year_week(2020, 1))
