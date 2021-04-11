# coding=utf8

import calendar
from datetime import date
import unittest

from borax.calendars.festivals2 import SolarFestival, LunarFestival, WeekFestival, TermFestival, decode, FestivalLibrary


class FestivalEncodeTestCase(unittest.TestCase):
    def test_festival_encode(self):
        new_year = SolarFestival(month=1, day=1)
        self.assertEqual('001010', new_year.encode())
        teacher_day = SolarFestival(month=9, day=10)
        self.assertEqual('009100', teacher_day.encode())
        lf2 = LunarFestival(month=5, day=5)
        self.assertEqual('105050', lf2.encode())
        month_day = WeekFestival(month=5, index=2, week=calendar.SUNDAY)
        self.assertEqual('205026', month_day.encode())
        tt = TermFestival(name='冬至')
        self.assertEqual('400230', tt.encode())
        sf2 = SolarFestival(day=-2)
        self.assertEqual('00002A', sf2.encode())
        lf3 = LunarFestival(day=-2)
        self.assertEqual('10002A', lf3.encode())

    def test_old_lunar(self):
        lf = decode('312011')
        lf2 = LunarFestival(month=12, day=-1)
        self.assertEqual(lf.encode(), lf2.encode())
        lf = decode('312010')
        lf2 = LunarFestival(month=12, day=1)
        self.assertEqual(lf.encode(), lf2.encode())


class FestivalDecodeTestCase(unittest.TestCase):
    def test_festival_decode(self):
        raw = '001010'
        f = decode(raw)
        self.assertEqual(raw, f.encode())
        raw2 = '0202001010'
        f2 = decode(raw2)
        self.assertEqual(raw, f2.encode())

    def test_fail_decode(self):
        with self.assertRaises(ValueError):
            decode('XEDE')
        with self.assertRaises(ValueError):
            decode('123456789')
        with self.assertRaises(ValueError):
            decode('654321')

    def test_all(self):
        all_codes = ['001010', '009100', '105050', '205026', '400230', '00002A', '00112A', '00003C']
        for raw in all_codes:
            with self.subTest(raw=raw):
                f = decode(raw)
                self.assertEqual(raw, f.encode())


class FestivalLibraryTestCase(unittest.TestCase):
    def test_library(self):
        fl = FestivalLibrary.from_builtin()
        self.assertEqual(27, len(fl))

        names = fl.get_festival_names(date_obj=date(2021, 10, 1))
        self.assertListEqual(['国庆节'], names)
