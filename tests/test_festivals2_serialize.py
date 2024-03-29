import calendar
import unittest
from datetime import date

from borax.calendars.festivals2 import SolarFestival, LunarFestival, WeekFestival, TermFestival, decode, \
    decode_festival, WrappedDate, FestivalError
from borax.calendars.lunardate import LunarDate


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
        lf = decode_festival('312011')
        lf2 = LunarFestival(month=12, day=-1)
        self.assertEqual(lf.encode(), lf2.encode())
        lf = decode_festival('312010')
        lf2 = LunarFestival(month=12, day=1)
        self.assertEqual(lf.encode(), lf2.encode())


class FestivalDecodeTestCase(unittest.TestCase):
    def test_festival_decode(self):
        raw = '001010'
        f = decode_festival(raw)
        self.assertEqual(raw, f.encode())
        raw2 = '0202001010'
        f2 = decode_festival(raw2)
        self.assertEqual(raw, f2.encode())

    def test_fail_decode(self):
        with self.assertRaises(ValueError):
            decode_festival('XEDE')
        with self.assertRaises(ValueError):
            decode_festival('123456789')
        with self.assertRaises(ValueError):
            decode_festival('654321')

    def test_all(self):
        all_codes = [
            '001010', '009100', '105050', '205026', '400230', '00002A', '00112A', '00003C', '201116',
            '411102', '421102', '43110B', '44110B']
        for raw in all_codes:
            with self.subTest(raw=raw):
                f = decode_festival(raw)
                self.assertEqual(raw, f.encode())
                self.assertEqual(raw, decode(raw).encode())


class DateEncoderTestCase(unittest.TestCase):
    def test_date_encode(self):
        ld = LunarDate(2021, 8, 15)
        self.assertEqual('1202108150', WrappedDate(ld).encode())
        self.assertEqual('0202109210', WrappedDate(ld.to_solar_date()).encode())

        ld = LunarDate(2020, 4, 3, 1)
        self.assertEqual('1202004031', WrappedDate(ld).encode())

    def test_date_decode(self):
        wd = WrappedDate.decode('0202109210')
        self.assertEqual(date(2021, 9, 21), wd.solar)

        wd1 = WrappedDate.decode('1202004031')
        self.assertEqual(LunarDate(2020, 4, 3, 1), wd1.lunar)

        wd2 = WrappedDate.decode('1202004030')
        self.assertEqual(LunarDate(2020, 4, 3, 0), wd2.lunar)

    def test_exception(self):
        with self.assertRaises(FestivalError):
            WrappedDate.decode('4202100230')
