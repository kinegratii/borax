# coding=utf8

import unittest

from borax.calendars.lunardate import (
    LunarDate, MAX_OFFSET,
    YEAR_DAYS, MIN_SOLAR_DATE,
    MAX_SOLAR_DATE
)


class BenchmarkTestCase(unittest.TestCase):
    def test_edge_dates(self):
        # Max date
        self.assertEqual(MAX_OFFSET, LunarDate.max.offset)
        self.assertEqual(MAX_OFFSET, (LunarDate.max - LunarDate.min).days)
        self.assertEqual(MAX_OFFSET + 1, sum(YEAR_DAYS))

        self.assertEqual(0, (LunarDate.min - MIN_SOLAR_DATE).days)
        self.assertEqual(0, (LunarDate.max - MAX_SOLAR_DATE).days)

        sd2100_ld = LunarDate.from_solar_date(2100, 12, 31)
        self.assertEqual('庚申年戊子月丁未日', sd2100_ld.gz_str())
        sd2101_ld = LunarDate.from_solar_date(2101, 1, 28)
        self.assertEqual('庚申年己丑月乙亥日', sd2101_ld.gz_str())
