# coding=utf8

import unittest
from datetime import date

from borax.calendars.festivals import (SolarSchema, LunarSchema, WeekSchema,
                                       TermSchema, DayLunarSchema, get_festival, DateSchemaFactory)
from borax.calendars.lunardate import LunarDate


class MixedDateTestCase(unittest.TestCase):
    def test_match(self):
        md = SolarSchema(year=0, month=2, day=14)
        self.assertTrue(md.match(date(2019, 2, 14)))
        self.assertTrue(md.match(date(2020, 2, 14)))
        self.assertFalse(md.match(date(2019, 2, 1)))

        md1 = LunarSchema(year=0, month=1, day=2)
        self.assertTrue(md1.match(LunarDate(2018, 1, 2)))

        with self.assertRaises(TypeError):
            md1.match(2)

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


class SchemaEncoderTestCase(unittest.TestCase):
    def test_encode(self):
        ss = SolarSchema.decode('0000012310')
        self.assertEqual(12, ss.month)
        self.assertEqual(31, ss.day)
        self.assertEqual(0, ss.reverse)
        self.assertEqual('0000012310', ss.encode())
        self.assertEqual('012310', ss.encode(short=True))

        ss1 = DateSchemaFactory.from_string('0000012310')
        self.assertEqual(12, ss1.month)
        self.assertEqual(31, ss1.day)
        self.assertEqual(0, ss1.reverse)
        self.assertEqual('0000012310', ss1.encode())
        self.assertEqual('012310', ss1.encode(short=True))

    def test_schema_factory(self):
        md2 = DateSchemaFactory.from_string('1000006140')
        self.assertTrue(md2.match(LunarDate(2017, 6, 14)))
        self.assertTrue(md2.match(LunarDate(2017, 6, 14, 1)))
        sd = LunarDate(2017, 6, 14).to_solar_date()
        self.assertTrue(md2.match(sd))

        md3 = DateSchemaFactory.from_string('106140')
        self.assertTrue(md3.match(LunarDate(2017, 6, 14)))
        self.assertTrue(md3.match(LunarDate(2017, 6, 14, 1)))
        sd = LunarDate(2017, 6, 14).to_solar_date()
        self.assertTrue(md3.match(sd))
