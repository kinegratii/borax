# coding=utf8

import unittest
from datetime import date

from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals import (date2mixed, mixed2date, SolarSchema, LunarSchema, WeekSchema,
                                       DateSchemaFactory, TermSchema, DayLunarSchema, get_festival)


class MixedDateTestCase(unittest.TestCase):
    def test_convert(self):
        self.assertEqual(date(2018, 2, 3), mixed2date('0201802030'))
        self.assertEqual(LunarDate(2017, 6, 4), mixed2date('1201706040'))
        self.assertEqual(LunarDate(2017, 6, 20, 1), mixed2date('1201706201'))

        self.assertEqual('0201802030', date2mixed(date(2018, 2, 3)))
        self.assertEqual('1201706040', date2mixed(LunarDate(2017, 6, 4)))
        self.assertEqual('1201706201', date2mixed(LunarDate(2017, 6, 20, 1)))
        with self.assertRaises(TypeError):
            date2mixed(2)

    def test_match(self):
        md = SolarSchema(year=0, month=2, day=14)
        self.assertTrue(md.match(date(2019, 2, 14)))
        self.assertTrue(md.match(date(2020, 2, 14)))
        self.assertFalse(md.match(date(2019, 2, 1)))

        md1 = LunarSchema(year=0, month=1, day=2)
        self.assertTrue(md1.match(LunarDate(2018, 1, 2)))

        with self.assertRaises(TypeError):
            md1.match(2)

        md2 = DateSchemaFactory.from_string('1000006140')
        self.assertTrue(md2.match(LunarDate(2017, 6, 14)))
        self.assertTrue(md2.match(LunarDate(2017, 6, 14, 1)))
        sd = LunarDate(2017, 6, 14).to_solar_date()
        self.assertTrue(md2.match(sd))

    def test_countdown_week(self):
        ws = WeekSchema(year=2019, month=5, index=2, week=6)
        self.assertTrue(ws.match(date(2019, 5, 12)))
        self.assertEqual(11, ws.countdown(date(2019, 5, 1)))
        self.assertEqual(1, ws.countdown(date(2019, 5, 11)))
        self.assertEqual(0, ws.countdown(date(2019, 5, 12)))
        self.assertEqual(363, ws.countdown(date(2019, 5, 13)))

    def test_countdown_solar(self):
        ss = SolarSchema(year=0, month=4, day=2)
        self.assertEqual(1, ss.countdown(date(2019, 4, 1)))
        self.assertEqual(0, ss.countdown(date(2019, 4, 2)))
        self.assertEqual(365, ss.countdown(date(2019, 4, 3)))

        ss1 = SolarSchema(year=2019, month=4, day=1, reverse=1)
        self.assertEqual(29, ss1.countdown(date(2019, 4, 1)))

        ss2 = SolarSchema(month=6, day=24)
        self.assertEqual(202, ss2.countdown(date(2007, 12, 5)))

    def test_countdown_lunar(self):
        ls = LunarSchema(year=0, month=4, day=2)
        self.assertEqual(1, ls.countdown(LunarDate(2019, 4, 1)))
        self.assertEqual(0, ls.countdown(LunarDate(2019, 4, 2)))
        self.assertEqual(353, ls.countdown(LunarDate(2019, 4, 3)))

    def test_countdown_term(self):
        ts = TermSchema(year=2019, index=6)
        self.assertEqual(4, ts.countdown(date(2019, 4, 1)))


class FuzzyTestCaseTest(unittest.TestCase):
    def test_fuzzy_feature(self):
        ss = SolarSchema(month=4, day=1)
        with self.assertRaises(ValueError):
            ss.resolve()
        self.assertEqual(date(2018, 4, 1), ss.resolve(2018))

        dls = DayLunarSchema(month=12, day=1, reverse=1)
        self.assertEqual(1, (LunarDate(2019, 1, 1) - dls.resolve(2018)).days)
        schema = get_festival('元旦')
        self.assertTrue(schema.match(date(2019, 1, 1)))


class ReverseTestCase(unittest.TestCase):
    def test_solar_february(self):
        ss = SolarSchema(year=2018, month=2, day=1, reverse=1)
        self.assertTrue(ss.match(date(2018, 2, 28)))

        ss1 = SolarSchema(month=2, day=1, reverse=1)
        self.assertTrue(ss1.match(date(2018, 2, 28)))
        self.assertEqual(27, ss1.delta(date(2020, 2, 2)))


class LeapIgnoreTestCase(unittest.TestCase):
    def test_match(self):
        ls = LunarSchema(month=6, day=1)
        self.assertTrue(ls.match(LunarDate(2017, 6, 1, 0)))
        self.assertTrue(ls.match(LunarDate(2017, 6, 1, 1)))

        ls1 = LunarSchema(month=6, day=1, ignore_leap=0)
        self.assertTrue(ls1.match(LunarDate(2017, 6, 1, 0)))
        self.assertFalse(ls1.match(LunarDate(2017, 6, 1, 1)))

        ls2 = LunarSchema(month=6, day=1, leap=1, ignore_leap=0)
        self.assertFalse(ls2.match(LunarDate(2017, 6, 1, 0)))
        self.assertTrue(ls2.match(LunarDate(2017, 6, 1, 1)))

    def test_leap_countdown(self):
        ls = LunarSchema(month=6, day=1)
        ls.delta(LunarDate(2017, 6, 27))
