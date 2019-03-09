# coding=utf8

import datetime
import unittest
from datetime import date, timedelta

from borax.calendars.lunardate import LunarDate, parse_year_days, LCalendars


class LunarDateTestCase(unittest.TestCase):
    def test_create_date(self):
        ld = LunarDate(1976, 8, 8, 1)
        self.assertEqual(1976, ld.year)
        self.assertEqual(8, ld.month)
        self.assertEqual(8, ld.day)
        self.assertEqual(True, ld.leap)

    def test_convert_datetime(self):
        dt = LunarDate(1976, 8, 8, 1).to_solar_date()
        self.assertEqual(date(1976, 10, 1), dt)
        dt2 = LunarDate.from_solar_date(2033, 10, 23)
        self.assertTrue(LunarDate(2033, 10, 1, 0), dt2)

        # day out of range
        with self.assertRaises(ValueError):
            LunarDate(2004, 1, 30).to_solar_date()

        # year out of range [1900, 2100]
        with self.assertRaises(ValueError):
            LunarDate(2101, 1, 1).to_solar_date()

        with self.assertRaises(ValueError):
            LunarDate(2019, 1, 1, 1).to_solar_date()

    def test_solar_and_lunar(self):
        ld = LunarDate.today()
        sd = ld.to_solar_date()
        self.assertEqual(ld.weekday(), sd.weekday())
        self.assertEqual(ld.isoweekday(), sd.isoweekday())

    def test_timedelta(self):
        ld = LunarDate(1976, 8, 8)
        sd = date(2008, 1, 1)
        td = timedelta(days=10)

        self.assertEqual(timedelta(days=0), ld - ld)
        self.assertEqual(LunarDate(1976, 7, 27, 0), ld - td)
        self.assertEqual(timedelta(11444), sd - ld)
        self.assertEqual(LunarDate(1976, 8, 18, 0), ld + td)
        self.assertEqual(LunarDate(1976, 8, 18, 0), td + ld)

    def test_comparison(self):
        ld = LunarDate(1976, 8, 8)
        ld2 = LunarDate.today()
        self.assertTrue(ld < ld2)
        self.assertTrue(ld <= ld2)
        self.assertTrue(ld2 > ld)
        self.assertTrue(ld2 >= ld)
        self.assertTrue(ld != ld2)
        self.assertFalse(ld == ld2)
        self.assertTrue(LunarDate.today() == LunarDate.today())

        # Compare with a integer
        self.assertFalse(LunarDate.today() == 5)
        with self.assertRaises(TypeError):
            LunarDate.today() < 5
        with self.assertRaises(TypeError):
            LunarDate.today() > 5
        with self.assertRaises(TypeError):
            LunarDate.today() >= 5
        with self.assertRaises(TypeError):
            LunarDate.today() >= 5

    def test_immutable_feature(self):
        ld1 = LunarDate(2018, 6, 1)
        ld2 = LunarDate(2018, 6, 1)
        self.assertEqual(1, len({ld1, ld2}))

    def test_term_ganzhi_feature(self):
        ld = LunarDate(2018, 6, 26)
        self.assertEqual(datetime.date(2018, 8, 7), ld.to_solar_date())
        self.assertEqual(43287, ld._offset)
        self.assertEqual('立秋', ld.term)
        self.assertEqual('戊戌', ld.gz_year)
        self.assertEqual('庚申', ld.gz_month)
        self.assertEqual('辛未', ld.gz_day)
        self.assertEqual('二〇一八年六月廿六', ld.cn_str())
        self.assertEqual('戊戌年庚申月辛未日', ld.gz_str())

        ld1 = LunarDate(2018, 12, 20)
        self.assertEqual('戊戌', ld1.gz_year)
        self.assertEqual('狗', ld.animal)

        ld2 = LunarDate(2018, 12, 10)
        self.assertEqual('初十', ld2.cn_day)

    def test_new_date(self):
        ld = LunarDate(2018, 12, 10)
        ld1 = ld.replace(year=2017, month=6, day=23, leap=1)
        self.assertEqual(2017, ld1.year)


class PrivateMethodsTestCase(unittest.TestCase):
    def test_year_info(self):
        self.assertEqual(348, parse_year_days(0))  # no leap month, and every month has 29 days.
        self.assertEqual(377, parse_year_days(1))  # 1 leap month, and every month has 29 days.
        self.assertEqual(360, parse_year_days((2 ** 12 - 1) * 16))  # no leap month, and every month has 30 days.
        self.assertEqual(390, parse_year_days((2 ** 13 - 1) * 16 + 1))  # 1 leap month, and every month has 30 days.
        # 1 leap month, and every normal month has 30 days, and leap month has 29 days.
        self.assertEqual(389, parse_year_days((2 ** 12 - 1) * 16 + 1))


class FormatterTestCase(unittest.TestCase):
    def test_valid_format(self):
        ld = LunarDate(2018, 4, 3)
        self.assertEqual('2018-4-3', ld.strftime('%y-%m-%d'))
        self.assertEqual('二〇一八', ld.strftime('%Y'))
        self.assertEqual('2018%c', ld.strftime('%y%c'))  # Just ignore %c, no raise error

        ld2 = LunarDate(2018, 11, 23)
        self.assertEqual('二〇一八/冬/廿三', ld2.strftime('%Y/%M/%D'))

        ld3 = LunarDate(2017, 6, 3, 1)
        self.assertEqual('61', ld3.strftime('%m%l'))
        self.assertEqual('闰六', ld3.strftime('%L%M'))
        self.assertEqual(ld3.gz_str(), ld3.strftime('%G'))

        self.assertEqual('%y', ld3.strftime('%%y'))
        self.assertEqual('%2017', ld3.strftime('%%%y'))
        self.assertEqual('2017631', ld3.strftime('%y%m%d%l'))
        self.assertEqual('201706031', ld3.strftime('%y%A%B%l'))


class LCalendarTestCase(unittest.TestCase):
    def test_ndays(self):
        self.assertEqual(354, LCalendars.ndays(2018))
        self.assertEqual(30, LCalendars.ndays(2018, 12))
        self.assertEqual(30, LCalendars.ndays(2017, 6, 1))
        with self.assertRaises(ValueError):
            LCalendars.ndays(2017, 7, 1)
        with self.assertRaises(ValueError):
            LCalendars.ndays(2017, 13)

    def test_leap_check(self):
        self.assertTrue(LCalendars.is_leap_month(2017, 6))
        self.assertFalse(LCalendars.is_leap_month(2017, 7))
        self.assertTrue(LCalendars.leap_month(2017) == 6)
        self.assertFalse(LCalendars.leap_month(2017) == 7)

    def test_delta(self):
        sd = date(2018, 12, 1)

        self.assertEqual(-1, LCalendars.delta(sd, date(2018, 12, 2)))
        self.assertEqual(-1, LCalendars.delta(LunarDate.from_solar(sd), date(2018, 12, 2)))
        self.assertEqual(4, LCalendars.delta(LunarDate(2018, 1, 6), LunarDate(2018, 1, 2)))
