# coding=utf8

import unittest
import datetime
from datetime import date, timedelta

from borax.calendars.lunardate import (
    LunarDate, parse_year_days, MAX_OFFSET,
    LCalendars, YEAR_DAYS, _START_SOLAR_DATE,
    _END_SOLAR_DATE
)


class BenchmarkTestCase(unittest.TestCase):
    def test_edge_dates(self):
        # Max date
        self.assertEqual(MAX_OFFSET, LunarDate.max.offset)
        self.assertEqual(MAX_OFFSET, (LunarDate.max - LunarDate.min).days)
        self.assertEqual(MAX_OFFSET + 1, sum(YEAR_DAYS))

        self.assertEqual(0, (LunarDate.min - _START_SOLAR_DATE).days)
        self.assertEqual(0, (LunarDate.max - _END_SOLAR_DATE).days)

        sd2100_ld = LunarDate.from_solar_date(2100, 12, 31)
        self.assertEqual('庚申年戊子月丁未日', sd2100_ld.gz_str())
        sd2101_ld = LunarDate.from_solar_date(2101, 1, 28)
        self.assertEqual('庚申年己丑月乙亥日', sd2101_ld.gz_str())
