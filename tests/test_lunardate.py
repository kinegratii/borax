# coding=utf8

import datetime
import unittest

from datetime import date, timedelta

from borax.calendars.lunardate import LunarDate, parse_year_days, ymdl2offset, offset2ymdl, _MAX_OFFSET


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
        self.assertEqual('二〇一八年六月廿六日', ld.cn_str())
        self.assertEqual('戊戌年庚申月辛未日', ld.gz_str())


class PrivateMethodsTestCase(unittest.TestCase):
    def test_year_info(self):
        self.assertEqual(348, parse_year_days(0))  # no leap month, and every month has 29 days.
        self.assertEqual(377, parse_year_days(1))  # 1 leap month, and every month has 29 days.
        self.assertEqual(360, parse_year_days((2 ** 12 - 1) * 16))  # no leap month, and every month has 30 days.
        self.assertEqual(390, parse_year_days((2 ** 13 - 1) * 16 + 1))  # 1 leap month, and every month has 30 days.
        # 1 leap month, and every normal month has 30 days, and leap month has 29 days.
        self.assertEqual(389, parse_year_days((2 ** 12 - 1) * 16 + 1))


class BenchmarkTestCase(unittest.TestCase):
    def test_ymdl_offset(self):
        """ offset2ymdl <=> ymdl2offset
        """
        for offset in range(0, _MAX_OFFSET + 1):
            y, m, d, l = offset2ymdl(offset)
            _offset = ymdl2offset(y, m, d, l)
            self.assertEqual(_offset, offset)

    def test_edge_dates(self):
        # Max date
        self.assertEqual(_MAX_OFFSET, LunarDate.max.offset)

        sd2100_ld = LunarDate.from_solar_date(2100, 12, 31)
        self.assertEqual('庚申年戊子月丁未日', sd2100_ld.gz_str())
