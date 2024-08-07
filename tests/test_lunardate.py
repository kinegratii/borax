import datetime
import unittest
from datetime import date, timedelta

from borax.calendars.lunardate import (
    LunarDate, parse_year_days, LCalendars, InvalidLunarDateError, TextUtils, TermUtils
)


class TextUtilsTestCase(unittest.TestCase):
    def test_cn_day_text(self):
        data = [
            (1, '初一'),
            (10, '初十'),
            (14, '十四'),
            (20, '二十'),
            (23, '廿三'),
            (30, '三十')
        ]
        for value, text in data:
            with self.subTest(value=value, text=text):
                self.assertEqual(text, TextUtils.day_cn(value))


class LunarDateTestCase(unittest.TestCase):
    def test_create_date(self):
        ld = LunarDate(1976, 8, 8, 1)
        self.assertEqual(1976, ld.year)
        self.assertEqual(8, ld.month)
        self.assertEqual(8, ld.day)
        self.assertEqual(1, ld.leap)

    def test_create_specific_dates(self):
        today = LunarDate.today()
        self.assertEqual(1, LCalendars.delta(LunarDate.tomorrow(), today))
        self.assertEqual(-1, LCalendars.delta(LunarDate.yesterday(), today))
        self.assertEqual(5, LCalendars.delta(today.after(5), today))
        self.assertEqual(-5, LCalendars.delta(today.before(5), today))

    def test_last_day(self):
        self.assertEqual(LunarDate(2023, 12, 30), LunarDate.last_day(2023))
        self.assertEqual(LunarDate(2023, 1, 29), LunarDate.last_day(2023, 1))
        self.assertEqual(LunarDate(2023, 2, 30), LunarDate.last_day(2023, 2))
        self.assertEqual(LunarDate(2023, 2, 29, 1), LunarDate.last_day(2023, 2, leap=1))
        self.assertEqual(LunarDate(2023, 3, 29), LunarDate.last_day(2023, 3))

        self.assertEqual(LunarDate(2024, 12, 29), LunarDate.last_day(2024))
        with self.assertRaises(Exception):
            LunarDate.last_day(2024, 2, 1)

    def test_convert_datetime(self):
        dt = LunarDate(1976, 8, 8, 1).to_solar_date()
        self.assertEqual(date(1976, 10, 1), dt)
        dt2 = LunarDate.from_solar_date(2033, 10, 23)
        self.assertTrue(LunarDate(2033, 10, 1, 0), dt2)

        # day out of range
        with self.assertRaises(InvalidLunarDateError):
            LunarDate(2004, 1, 30).to_solar_date()

        # year out of range [1900, 2100]
        with self.assertRaises(InvalidLunarDateError):
            LunarDate(2101, 1, 1).to_solar_date()

        with self.assertRaises(InvalidLunarDateError):
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
        # Act as dict keys
        dic = {ld1: 'day1'}
        self.assertEqual('day1', dic.get(ld1))
        ld3 = LunarDate(2018, 6, 1)
        self.assertEqual('day1', dic.get(ld3))
        dic[ld3] = 'day2'
        self.assertEqual(1, len(dic))
        self.assertEqual('day2', dic.get(ld1))

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

    def test_term_of_edge_years(self):
        sd = LCalendars.create_solar_date(2101, 0)
        self.assertEqual(date(2101, 1, 5), sd)
        ld = LunarDate.from_solar(sd)
        self.assertEqual('小寒', ld.term)

        sd1 = TermUtils.nth_term_day(2101, 1)
        self.assertEqual(date(2101, 1, 20), sd1)
        ld1 = LunarDate.from_solar(sd1)
        self.assertEqual('大寒', ld1.term)

        with self.assertRaises(ValueError):
            LCalendars.create_solar_date(2101, 2)

    def test_day_start_from_term(self):
        day = TermUtils.day_start_from_term(2022, '芒种', 1, '甲')
        self.assertEqual(date(2022, 6, 10), day)
        day2 = TermUtils.day_start_from_term(2022, '小暑', 1, '未')
        self.assertEqual(date(2022, 7, 17), day2)
        day3 = TermUtils.day_start_from_term(2022, '芒种', 0, '未')
        self.assertEqual(date(2022, 6, 6), day3)
        with self.assertRaises(ValueError):
            TermUtils.day_start_from_term(2022, '冬至', 2, '某')


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
        self.assertEqual('2018%z', ld.strftime('%y%z'))  # Just ignore %c, no raise error

        ld2 = LunarDate(2018, 11, 23)
        self.assertEqual('二〇一八/冬/廿三', ld2.strftime('%Y/%M/%D'))
        self.assertEqual('二〇一八/十一/廿三', ld2.strftime('%Y/%N/%D'))
        self.assertEqual('廿三', ld2.strftime('%F'))

        ld3 = LunarDate(2017, 6, 3, 1)
        self.assertEqual('61', ld3.strftime('%m%l'))
        self.assertEqual('闰六', ld3.strftime('%L%M'))
        self.assertEqual(ld3.gz_str(), ld3.strftime('%G'))

        self.assertEqual('%y', ld3.strftime('%%y'))
        self.assertEqual('%2017', ld3.strftime('%%%y'))
        self.assertEqual('2017631', ld3.strftime('%y%m%d%l'))
        self.assertEqual('201706031', ld3.strftime('%y%A%B%l'))
        self.assertEqual('201706031', ld3.__format__('%y%A%B%l'))

    def test_term(self):
        ld = LunarDate(2020, 3, 23)
        self.assertEqual('tem:-', ld.strftime('tem:%t'))

    def test_cn_calendar_day(self):
        ld = LunarDate(2017, 6, 1, 1)
        self.assertEqual('闰六月', ld.strftime('%F'))
        ld1 = LunarDate(2017, 11, 1, 0)
        self.assertEqual('十一月', ld1.strftime('%F'))

    def test_cn_week(self):
        ld = LunarDate(2022, 8, 15)
        self.assertEqual('六', ld.strftime('%W'))
        ld2 = ld + timedelta(days=1)
        self.assertEqual('日', ld2.strftime('%W'))


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
        self.assertTrue(LCalendars.leap_month(2017) == 6)
        self.assertFalse(LCalendars.leap_month(2017) == 7)
        self.assertIn(2017, LCalendars.get_leap_years(6))
        self.assertIn(2017, LCalendars.get_leap_years())
        self.assertEqual(0, len(LCalendars.get_leap_years(14)))

    def test_delta(self):
        sd = date(2018, 12, 1)

        self.assertEqual(-1, LCalendars.delta(sd, date(2018, 12, 2)))
        self.assertEqual(-1, LCalendars.delta(LunarDate.from_solar(sd), date(2018, 12, 2)))
        self.assertEqual(4, LCalendars.delta(LunarDate(2018, 1, 6), LunarDate(2018, 1, 2)))


class GZTestCase(unittest.TestCase):
    def test_gz_str(self):
        for offset in range(60):
            text = TextUtils.offset2gz(offset)
            ex_offset = TextUtils.gz2offset(text)
            self.assertEqual(ex_offset, offset)

        with self.assertRaises(ValueError):
            TextUtils.gz2offset('甲丑')  # No gz string
