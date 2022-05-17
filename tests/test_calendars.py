# coding=utf8


import unittest
from datetime import date, timedelta

from borax.calendars.lunardate import LunarDate
from borax.calendars.utils import SCalendars, ThreeNineUtils


class LastDayTestCase(unittest.TestCase):
    def test_last_day(self):
        self.assertEqual(date(2019, 3, 31), SCalendars.get_last_day_of_this_month(2019, 3))
        self.assertEqual(date(2019, 2, 28), SCalendars.get_last_day_of_this_month(2019, 2))
        self.assertEqual(date(2020, 2, 29), SCalendars.get_last_day_of_this_month(2020, 2))

    def test_fist_day_of_week(self):
        self.assertEqual(date(2020, 2, 24), SCalendars.get_fist_day_of_year_week(2020, 8))
        self.assertEqual(date(2020, 1, 6), SCalendars.get_fist_day_of_year_week(2020, 1))


class ThreeNineTestCase(unittest.TestCase):
    def test_get_39label(self):
        self.assertEqual('九九第1天', ThreeNineUtils.get_39label(date(2022, 3, 3)))
        self.assertEqual('', ThreeNineUtils.get_39label(date(2022, 4, 12)))
        self.assertEqual('九九第1天', ThreeNineUtils.get_39label(LunarDate.from_solar(date(2022, 3, 3))))
        self.assertEqual('中伏第1天', ThreeNineUtils.get_39label(date(2021, 7, 21)))

    def test_39label_for_one_day(self):
        d = ThreeNineUtils.get_39days(2022)['初伏']
        self.assertEqual(date(2022, 7, 16), d)
        self.assertEqual('庚', LunarDate.from_solar(d).gz_day[0])
        self.assertEqual('初伏第10天', ThreeNineUtils.get_39label(d + timedelta(days=9)))
        self.assertEqual('中伏第1天', ThreeNineUtils.get_39label(d + timedelta(days=10)))
        self.assertEqual('', ThreeNineUtils.get_39label(date(2021, 9, 30)))
