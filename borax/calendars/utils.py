# coding=utf8
import calendar
from datetime import date, datetime, timedelta

from borax.calendars.lunardate import LunarDate, LCalendars, TextUtils

from typing import Union

__all__ = ['SCalendars', 'ThreeNineUtils']


class SCalendars:
    @staticmethod
    def get_last_day_of_this_month(year: int, month: int) -> date:
        return date(year, month, calendar.monthrange(year, month)[-1])

    @staticmethod
    def get_fist_day_of_year_week(year: int, week: int) -> date:
        fmt = '{}-W{}-1'.format(year, week)
        return datetime.strptime(fmt, "%Y-W%W-%w").date()


class ThreeNineUtils:
    @staticmethod
    def get_start_date(year, term_name, after_index, day_stem):
        term_day = LCalendars.create_solar_date(year, term_name=term_name)
        term_lday = LunarDate.from_solar(term_day)
        term_stem_index = TextUtils.STEMS.find(term_lday.gz_day[0])
        day_stem_index = TextUtils.STEMS.find(day_stem)
        day_offset = (day_stem_index - term_stem_index) + 10 * bool(6 - term_stem_index) + 10 * (after_index - 1)
        return term_day + timedelta(days=day_offset)

    @staticmethod
    def get_39days(year: int) -> dict[str, date]:
        day13 = ThreeNineUtils.get_start_date(year, '夏至', 3, '庚')
        day23 = day13 + timedelta(days=10)
        day33 = ThreeNineUtils.get_start_date(year, '立秋', 1, '庚')
        day19 = ThreeNineUtils.get_start_date(year, '冬至', 1, '壬')
        days = {
            '初伏': day13,
            '中伏': day23,
            '末伏': day33,
            '一九': day19
        }
        for i, dc in enumerate(TextUtils.DAYS_CN[1:10], start=1):
            days['{}九'.format(dc)] = day19 + timedelta(days=(i - 1) * 9)
        return days

    @staticmethod
    def get_39label(date_obj: Union[date, LunarDate]) -> str:
        if isinstance(date_obj, LunarDate):
            sd = date_obj.to_solar_date()
        else:
            sd = date_obj
        if sd.month in (4, 5, 6, 10, 11):
            return ''
        year = sd.year - bool(sd.month < 4)
        days = ThreeNineUtils.get_39days(year)
        return {v: k for k, v in days.items()}.get(sd, '')
