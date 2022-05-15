# coding=utf8

import calendar
import unittest
from datetime import date, timedelta

from borax.calendars.festivals2 import SolarFestival, LunarFestival, WeekFestival, TermFestival, FestivalError, \
    FreqConst, Period, WrappedDate
from borax.calendars.lunardate import LunarDate, LCalendars


class SolarFestivalTestCase(unittest.TestCase):
    def test_yearly(self):
        sf = SolarFestival(month=2, day=4)
        month, day = sf.gets('month', 'day')
        self.assertEqual(2, month)
        self.assertEqual(4, day)
        freq = sf.gets('freq')
        self.assertEqual(0, freq)
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

        sf2 = SolarFestival(day=-2)
        self.assertEqual(date(2020, 12, 30), sf2.at(year=2020))

    def test_monthly(self):
        sf = SolarFestival(freq=FreqConst.MONTHLY, day=3)
        self.assertEqual(date(2021, 2, 3), sf.at(year=2021, month=2))
        self.assertEqual(date(2021, 3, 3), sf.at(year=2021, month=3))
        with self.assertRaises(FestivalError):
            sf.at(year=2021)

    def test_reverse(self):
        sf = SolarFestival(month=12, day=-1)
        self.assertEqual(date(2021, 12, 31), sf.at(2021))

        sf2 = SolarFestival(freq=FreqConst.MONTHLY, day=-1)
        self.assertEqual(date(2021, 3, 31), sf2.at(year=2021, month=3))
        self.assertEqual(date(2021, 2, 28), sf2.at(year=2021, month=2))
        self.assertEqual(date(2020, 2, 29), sf2.at(year=2020, month=2))


class WeekFestivalTestCase(unittest.TestCase):
    def test_basic_logic(self):
        month_day = WeekFestival(month=5, index=2, week=calendar.SUNDAY, name='母亲节')
        monthday2021 = month_day.at(year=2021)
        self.assertEqual(date(2021, 5, 9), monthday2021)

        monthday2021_1 = month_day.at(year=2021, month=5)
        self.assertEqual(date(2021, 5, 9), monthday2021_1)

        with self.assertRaises(FestivalError):
            month_day.at(year=2021, month=3)

    def test_monthly(self):
        # Add in v3.5.6
        last_sunday = WeekFestival(month=0, index=-1, week=6)
        self.assertEqual(date(2022, 4, 24), last_sunday.at(2022, 4))
        self.assertEqual(12, len(last_sunday.list_days(*Period.solar_year(2022))))

        week_festival2 = WeekFestival(month=0, index=5, week=6)
        self.assertEqual(4, len(week_festival2.list_days(*Period.solar_year(2022))))


class TermFestivalTestCase(unittest.TestCase):
    def test_basic_logic(self):
        tt = TermFestival(name='立春')
        self.assertEqual(date(2021, 2, 3), tt.at(year=2021))

        with self.assertRaises(FestivalError):
            tt.at(year=2021, month=3)


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

        sf2 = LunarFestival(day=-1)
        self.assertEqual(LunarDate(2020, 12, 30), sf2.at(year=2020))

    def test_monthly(self):
        lf = LunarFestival(freq=FreqConst.MONTHLY, day=3)
        self.assertEqual(LunarDate(2021, 2, 3), lf.at(year=2021, month=2))
        self.assertEqual(LunarDate(2021, 3, 3), lf.at(year=2021, month=3))
        with self.assertRaises(FestivalError):
            lf.at(year=2021)


class CheckFestivalTestCase(unittest.TestCase):
    def test_all_days(self):
        ld = LunarDate(2021, 1, 3)
        lf = LunarFestival(day=3)
        self.assertTrue(lf.is_(ld))


class PeriodTestCase(unittest.TestCase):
    def test_solar_period(self):
        sd1, ed1 = Period.solar_year(2020)
        self.assertEqual(date(2020, 1, 1), sd1)
        self.assertEqual(date(2020, 12, 31), ed1)

        sd2, ed2 = Period.solar_month(2020, 5)
        self.assertEqual(date(2020, 5, 1), sd2)
        self.assertEqual(date(2020, 5, 31), ed2)

    def test_lunar_period(self):
        sd1, ed1 = Period.lunar_year(2020)
        self.assertEqual(LunarDate(2020, 1, 1), sd1)
        self.assertEqual(LunarDate(2020, 12, 30), ed1)

        sd2, ed2 = Period.lunar_month(2020, 4)
        self.assertEqual(LunarDate(2020, 4, 1, 0), sd2)
        self.assertEqual(LunarDate(2020, 4, 29, 1), ed2)

        sd3, ed3 = Period.lunar_month(2020, 4, leap=0)
        self.assertEqual(LunarDate(2020, 4, 1, 0), sd3)
        self.assertEqual(LunarDate(2020, 4, 30, 0), ed3)

        sd4, ed4 = Period.lunar_month(2020, 4, leap=1)
        self.assertEqual(LunarDate(2020, 4, 1, 1), sd4)
        self.assertEqual(LunarDate(2020, 4, 29, 1), ed4)

        sd5, ed5 = Period.lunar_month(2020, 5, leap=0)
        self.assertEqual(LunarDate(2020, 5, 1, 0), sd5)
        self.assertEqual(LunarDate(2020, 5, 30, 0), ed5)


class WrappedDateTestCase(unittest.TestCase):

    def test_wrapped_date(self):
        wd = WrappedDate(date(2021, 5, 1))
        sd, ld = wd
        self.assertEqual(date(2021, 5, 1), sd)
        self.assertEqual(LunarDate(2021, 3, 20), ld)

    def test_magic_method(self):
        WrappedDate(date(2021, 5, 1))

    def test_add(self):
        wd = WrappedDate(date(2021, 5, 1))
        self.assertEqual(date(2021, 5, 3), (wd + timedelta(days=2)).solar)
        self.assertEqual(date(2021, 5, 3), (timedelta(days=2) + wd).solar)

    def test_sub(self):
        wd = WrappedDate(date(2021, 5, 1))

        self.assertEqual(timedelta(days=2), date(2021, 5, 3) - wd)
        self.assertEqual(timedelta(days=1), wd - date(2021, 4, 30))

        self.assertEqual(timedelta(days=1), LunarDate(2021, 3, 21) - wd)
        self.assertEqual(timedelta(days=2), wd - LunarDate(2021, 3, 18))
        self.assertEqual(WrappedDate(date(2021, 4, 30)), wd - timedelta(days=1))

    def test_wd(self):
        wd = WrappedDate(LunarDate(2022, 4, 1))
        self.assertEqual('四月初一', wd.lunar.cn_md)
        ss = wd.simple_str()
        wd2 = WrappedDate.from_simple_str(ss)
        self.assertEqual(wd2.simple_str(), ss)


class FestivalListDaysTestCase(unittest.TestCase):
    def test_solar(self):
        sf = SolarFestival(day=256)
        days = list(sf.list_days(start_date=date(2020, 1, 1), end_date=date(2024, 1, 1)))
        self.assertEqual(4, len(days))
        self.assertEqual(date(2020, 9, 12), days[0].solar)
        self.assertEqual(date(2021, 9, 13), days[1].solar)
        self.assertEqual(date(2022, 9, 13), days[2].solar)
        self.assertEqual(date(2023, 9, 13), days[3].solar)

        days2 = list(sf.list_days(start_date=date(2020, 1, 1), end_date=date(2024, 1, 1), reverse=True))
        self.assertEqual(4, len(days2))
        self.assertEqual(date(2020, 9, 12), days2[3].solar)
        self.assertEqual(date(2021, 9, 13), days2[2].solar)
        self.assertEqual(date(2022, 9, 13), days2[1].solar)
        self.assertEqual(date(2023, 9, 13), days2[0].solar)

    def test_solar_monthly(self):
        sf2 = SolarFestival(freq=FreqConst.MONTHLY, day=-1)
        days = list(sf2.list_days(start_date=date(2020, 1, 1), end_date=date(2024, 1, 1)))
        solar_days = [d.solar for d in days]
        self.assertEqual(date(2020, 1, 31), solar_days[0])
        self.assertEqual(date(2023, 12, 31), solar_days[-1])

        sf2 = SolarFestival(freq=FreqConst.MONTHLY, day=-1)
        days = list(sf2.list_days(start_date=date(2020, 1, 1), end_date=date(2024, 1, 1), reverse=True))
        solar_days = [d.solar for d in days]
        self.assertEqual(date(2020, 1, 31), solar_days[-1])
        self.assertEqual(date(2023, 12, 31), solar_days[0])

    def test_week_festival(self):
        end_date = date(2024, 1, 1)
        month_day = WeekFestival(month=5, index=2, week=calendar.SUNDAY, name='母亲节')
        days = list(month_day.list_days(start_date=date(2020, 1, 1), end_date=end_date))
        self.assertEqual(4, len(days))

        self.assertEqual(calendar.MONDAY, end_date.weekday())
        first_monday_of_year = WeekFestival(month=1, index=1, week=calendar.MONDAY)
        days = list(first_monday_of_year.list_days(start_date=date(2020, 1, 1), end_date=end_date))
        self.assertEqual(5, len(days))

    def test_lunar(self):
        lf = LunarFestival(month=12, day=-1)
        days2 = list(lf.list_days(start_date=LunarDate(2014, 2, 3), end_date=LunarDate(2022, 1, 1)))
        self.assertEqual(8, len(days2))

        days3 = list(lf.list_days(start_date=LunarDate(2014, 2, 3), end_date=LunarDate(2021, 12, 29)))
        self.assertEqual(8, len(days3))

    def test_lunar_monthly(self):
        self.assertEqual(4, LCalendars.leap_month(2020))
        lf = LunarFestival(freq=FreqConst.MONTHLY, day=-1)
        days3 = list(lf.list_days(start_date=LunarDate(2020, 1, 1), end_date=LunarDate(2021, 1, 1)))
        self.assertEqual(13, len(days3))
        lunar_days3 = [d.lunar for d in days3]
        self.assertIn(LunarDate(2020, 4, 30, 0), lunar_days3)
        self.assertIn(LunarDate(2020, 4, 29, 1), lunar_days3)

        days4 = list(lf.list_days(start_date=LunarDate(2020, 1, 1), end_date=LunarDate(2021, 1, 1), reverse=True))
        self.assertEqual(13, len(days4))

        lf2 = LunarFestival(freq=FreqConst.MONTHLY, day=-1, leap=0)
        days5 = list(lf2.list_days(start_date=LunarDate(2020, 1, 1), end_date=LunarDate(2021, 1, 1)))
        self.assertEqual(12, len(days5))
        lunar_days5 = [d.lunar for d in days5]
        self.assertIn(LunarDate(2020, 4, 30, 0), lunar_days5)
        self.assertNotIn(LunarDate(2020, 4, 29, 1), lunar_days5)

    def test_week_out(self):
        wf = WeekFestival(month=1, index=7, week=calendar.MONDAY)
        days = list(wf.list_days(start_date=date(2020, 1, 1), end_date=date(2024, 1, 1)))
        self.assertEqual(0, len(days))

    def test_cast(self):
        sf = SolarFestival(day=256)
        ld = LunarDate.from_solar_date(2020, 1, 1)
        days = list(sf.list_days(start_date=ld, end_date=date(2024, 1, 1)))
        self.assertEqual(4, len(days))

    def test_future_and_past(self):
        new_year_festival = SolarFestival(month=1, day=1)
        new_year_day = list(new_year_festival.list_days_in_future(count=1))[0]
        today = date.today()
        self.assertTrue(0 <= new_year_day.solar.year - today.year <= 1)
        this_new_year = list(new_year_festival.list_days_in_past(count=1, reverse=True))[0]
        self.assertTrue(0 <= today.year - this_new_year.solar.year <= 1)

    def test_week_reverse(self):
        fs = WeekFestival(month=1, index=-1, week=calendar.SUNDAY)
        self.assertEqual(date(2022, 1, 30), fs.at(2022))


class CountdownTestCase(unittest.TestCase):
    def test_countdown(self):
        self.festival = SolarFestival(day=256)
        sf = self.festival
        nday, gd = sf.countdown(date(2020, 1, 1))
        self.assertEqual(255, nday)


class FestivalDescriptionTestCase(unittest.TestCase):
    def test_term_and_week_festivals(self):
        tf = TermFestival(index=1)
        self.assertEqual('公历每年大寒节气', tf.description)

        month_day = WeekFestival(month=5, index=2, week=calendar.SUNDAY, name='母亲节')
        self.assertEqual('公历5月第2个星期日', month_day.description)
        self.assertEqual('母亲节 公历5月第2个星期日', str(month_day))
        self.assertEqual('<WeekFestival 母亲节 公历5月第2个星期日>', repr(month_day))

    def test_solar_festival(self):
        festival2description_tuples = [
            (SolarFestival(month=1, day=1), '公历每年1月1日'),
            (SolarFestival(month=1, day=-1), '公历每年1月倒数第1天'),
            (SolarFestival(day=1), '公历每年第1天'),
            (SolarFestival(day=-1), '公历每年倒数第1天'),
            (SolarFestival(freq=FreqConst.MONTHLY, day=1), '公历每月1日'),
            (SolarFestival(freq=FreqConst.MONTHLY, day=-1), '公历每月倒数第1天')
        ]
        for f, d in festival2description_tuples:
            with self.subTest(f=f, d=d):
                self.assertEqual(d, f.description)

    def test_lunar_festival(self):
        festival2description_tuples = [
            (LunarFestival(month=1, day=1), '农历每年正月初一'),
            (LunarFestival(month=1, day=-1), '农历每年正月倒数第1天'),
            (LunarFestival(day=1), '农历每年第1天'),
            (LunarFestival(day=-1), '农历每年倒数第1天'),
            (LunarFestival(freq=FreqConst.MONTHLY, day=1), '农历每月初一'),
            (LunarFestival(freq=FreqConst.MONTHLY, day=-1), '农历每月倒数第1天')
        ]
        for f, d in festival2description_tuples:
            with self.subTest(f=f, d=d):
                self.assertEqual(d, f.description)
