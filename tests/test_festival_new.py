# coding=utf8

import calendar
import unittest
from datetime import date

from borax.calendars.festivals2 import SolarFestival, LunarFestival, WeekFestival, TermFestival, FestivalError, \
    MONTHLY
from borax.calendars.lunardate import LunarDate


class SolarFestivalTestCase(unittest.TestCase):
    def test_yearly(self):
        sf = SolarFestival(month=2, day=4)
        self.assertEqual(date(2021, 2, 4), sf.at(year=2021))
        self.assertEqual(date(2021, 2, 4), sf.at(year=2021, month=2))
        with self.assertRaises(FestivalError):
            sf.at(year=2021, month=3)

    def test_yearly_day_in_year(self):
        sf = SolarFestival(day=45)
        self.assertEqual(date(2021, 2, 14), sf.at(year=2021))
        self.assertEqual(date(2021, 2, 14), sf.at(year=2021, month=2))
        with self.assertRaises(FestivalError):
            sf.at(year=2021, month=3)

    def test_monthly(self):
        sf = SolarFestival(freq=MONTHLY, day=3)
        self.assertEqual(date(2021, 2, 3), sf.at(year=2021, month=2))
        self.assertEqual(date(2021, 3, 3), sf.at(year=2021, month=3))
        with self.assertRaises(FestivalError):
            sf.at(year=2021)


class WeekFestivalTestCase(unittest.TestCase):
    def test_basic_logic(self):
        month_day = WeekFestival(month=5, index=2, week=calendar.SUNDAY, name='母亲节')
        monthday2021 = month_day.at(year=2021)
        self.assertEqual(date(2021, 5, 9), monthday2021)

        monthday2021_1 = month_day.at(year=2021, month=5)
        self.assertEqual(date(2021, 5, 9), monthday2021_1)

        with self.assertRaises(FestivalError):
            month_day.at(year=2021, month=3)


class TermFestivalTestCase(unittest.TestCase):
    def test_basic_logic(self):
        tt = TermFestival(name='立春')
        self.assertEqual(date(2021, 2, 3), tt.at(year=2021))

        with self.assertRaises(FestivalError):
            tt.at(year=2021, month=3)


#
class LunarFestivalTestCase(unittest.TestCase):
    def test_yearly(self):
        spring_festival = LunarFestival(month=1, day=1).set_name('春节')
        self.assertEqual(LunarDate(2021, 1, 1), spring_festival.at(year=2021))
        self.assertEqual(LunarDate(2021, 1, 1), spring_festival.at(year=2021, month=1))
        with self.assertRaises(FestivalError):
            spring_festival.at(year=2021, month=3)

    def test_yearly_in_days(self):
        lf = LunarFestival(day=40)
        self.assertEqual(LunarDate(2021, 2, 11), lf.at(year=2021))
        self.assertEqual(LunarDate(2021, 2, 11), lf.at(year=2021, month=2))
        with self.assertRaises(FestivalError):
            lf.at(year=2021, month=3)

    def test_monthly(self):
        lf = LunarFestival(freq=MONTHLY, day=3)
        self.assertEqual(LunarDate(2021, 2, 3), lf.at(year=2021, month=2))
        self.assertEqual(LunarDate(2021, 3, 3), lf.at(year=2021, month=3))
        with self.assertRaises(FestivalError):
            lf.at(year=2021)
