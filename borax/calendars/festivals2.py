# coding=utf-8

import calendar
import enum
from datetime import date
from typing import Union, List

from borax.calendars.lunardate import LunarDate, LCalendars

MixedDate = Union[date, LunarDate]

(YEARLY, MONTHLY) = list(range(2))

# Private Global Variables

_IGNORE_LEAP_MONTH = 3


class FestivalSchema(enum.IntEnum):
    SOLAR = 0
    LUNAR = 1
    WEEK = 2
    LUNAR_OLD = 3  # 兼容旧版本
    TERM = 4


class FestivalError(Exception):
    def __init__(self, label, message, **kwargs):
        self._label = label
        self.message = '{}:{}'.format(label, message)
        super().__init__(self.message)


class Festival:
    date_class = None

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name', '')
        self._month = kwargs.get('month', 0)
        self._day = kwargs.get('day', 0)
        self._reverse = kwargs.get('reverse', 0)
        self._leap = kwargs.get('leap', _IGNORE_LEAP_MONTH)  # Only available if self._month != 0
        self._week_index = kwargs.get('index', 0)
        self._term_index = kwargs.get('index', 0)
        self._week_no = kwargs.get('week', 0)
        self._freq = kwargs.get('freq', 0)

    def set_name(self, name):
        self._name = name
        return self

    def is_(self, date_obj: MixedDate) -> bool:
        date_obj = self._normalize(date_obj)
        leap = getattr(date_obj, 'leap', 0)
        return (self.at(date_obj.year, date_obj.month, leap) - date_obj).days == 0

    def at(self, year: int, month: int = 0, leap=0) -> MixedDate:
        try:
            date_list = self._resolve(year, month, leap)
        except FestivalError:
            raise
        if len(date_list) == 0:
            raise FestivalError('DateDoesNotExit', '')
        elif len(date_list) > 1:
            raise FestivalError('MultipleDateExist', '')
        return date_list[0]

    def _resolve(self, year: int, month: int = 0, leap=0) -> List[Union[date, LunarDate]]:
        _y = year
        if month != 0 and self._month != 0 and month != self._month:
            raise FestivalError('DateDoesNotExist', 'Date does not exist.')
        if self._freq == MONTHLY and self._month == 0:
            _m = month
        else:
            _m = self._month

        try:
            if self._freq == YEARLY:
                obj_or_tuples = self._resolve_yearly(_y)
            else:
                obj_or_tuples = self._resolve_monthly(_y, _m, leap)
        except FestivalError:
            raise
        if isinstance(obj_or_tuples, (LunarDate, date)):
            date_list = obj_or_tuples,
        else:
            date_list = obj_or_tuples
        if month != 0:
            new_date_list = []
            for date_obj in date_list:
                is_match = (year, month) == (date_obj.year, date_obj.month) and (
                    self.date_class == date or leap == date_obj.leap)
                if is_match:
                    new_date_list.append(date_obj)
            return new_date_list
        else:
            return date_list

    def list_days(self, start_date=None, end_date=None, reverse=False):
        """
        list_days(solar_year=2021)
        list_days(solar_year=2021, solar_month=2)
        list_days(lunar_year=2021)
        list_days(lunar_year=2021, lunar_month=2)
        list_days(lunar_year=2021, lunar_month=2, include_leap=1)
        list_days(lunar_year=2021, lunar_month=2, leap=1)

        :param start_date:
        :param end_date:
        :return:
        """
        if start_date is None:
            start_date = self._normalize(LunarDate.min)
        if end_date is None:
            end_date = self._normalize(LunarDate.max)
        if self._freq == YEARLY:
            for day in self._list_yearly(start_date, end_date, reverse):
                if start_date <= day <= end_date:
                    yield day
        else:
            for day in self._list_monthly(start_date, end_date, reverse):
                if start_date <= day <= end_date:
                    yield day

    def _list_yearly(self, start_date, end_date, reverse):
        sy = start_date.year
        ey = end_date.year
        if reverse:
            iter = range(ey, sy - 1, -1)
        else:
            iter = range(sy, ey + 1)
        for year in iter:
            try:
                obj_list = self._resolve(year)
                for day in obj_list:
                    yield day
            except FestivalError:
                continue

    def _list_monthly(self, start_date, end_date, reverse):
        return []

    def _normalize(self, date_obj):
        date_class = self.date_class
        return LCalendars.cast_date(date_obj, date_class)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        return []

    def _resolve_monthly(self, year, month, leap=0) -> List[Union[date, LunarDate]]:
        return []


class SolarFestival(Festival):
    date_class = date

    def __init__(self, *, day, freq=YEARLY, month=0, name=None):
        if day < 0:
            day = -day
            reverse = 1
        else:
            reverse = 0
        super().__init__(name=name, freq=freq, month=month, day=day, reverse=reverse)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        # mock
        if self._month == 0:
            if self._reverse == 0:
                _index = self._day
            else:
                _index = 366 + int(calendar.isleap(year)) - self._day
            for month in range(1, 13):
                ndays = calendar.monthrange(year, month)[1]
                if _index <= ndays:
                    return [date(year, month, _index)]
                else:
                    _index -= ndays
        else:
            if self._reverse == 0:
                day = self._day
            else:
                day = calendar.monthrange(year, self._month)[1] - self._day + 1
            return [date(year, self._month, day)]

    def _resolve_monthly(self, year, month, leap=0) -> List[Union[date, LunarDate]]:

        if month == 0:
            data = []
            for m in range(1, 13):
                if self._reverse == 0:
                    day = self._day
                else:
                    day = calendar.monthrange(year, m)[1] - self._day + 1
                data.append(date(year, m, day))
            return data
        else:
            if self._reverse == 0:
                day = self._day
            else:
                day = calendar.monthrange(year, self._month)[1] - self._day + 1
            return [date(year, month, day)]


class WeekFestival(Festival):
    date_class = date

    def __init__(self, *, month, index, week, name=None):
        super().__init__(name=name, freq=YEARLY, month=month, index=index, week=week)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        day = WeekFestival.week_day(year, self._month, self._week_index, self._week_no)
        return [date(year, self._month, day)]

    @staticmethod
    def week_day(year: int, month: int, index: int, week: int) -> int:
        w, ndays = calendar.monthrange(year, month)
        if week >= w:
            d0 = week - w + 1
        else:
            d0 = 8 - (w - week)
        d = d0 + 7 * (index - 1)
        if not (1 <= d <= ndays):
            raise FestivalError("DateDoesNotExist", "")
        return d


class TermFestival(Festival):
    date_class = date

    def __init__(self, *, index=None, name=None):
        super().__init__(freq=YEARLY, name=name, index=index)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        return [LCalendars.create_solar_date(year, term_index=self._term_index, term_name=self._name)]


class LunarFestival(Festival):
    date_class = LunarDate

    def __init__(self, *, day, freq=YEARLY, month=0, leap=_IGNORE_LEAP_MONTH, name=None):
        if day < 0:
            day = -day
            reverse = 1
        else:
            reverse = 0
        super().__init__(freq=freq, name=name, month=month, day=day, leap=leap, reverse=reverse)

    def _resolve_yearly(self, year: int) -> List[Union[date, LunarDate]]:
        month_meta = LCalendars.iter_year_month(year)

        if self._month == 0:
            if self._reverse == 0:
                _index = self._day
            else:
                ndays_of_year = sum([t[1] for t in month_meta])
                _index = ndays_of_year - self._day + 1  # check ValueError
            for _m, _nd, _l in month_meta:
                if _index <= _nd:
                    return [LunarDate(year, _m, _index, _l)]
                else:
                    _index -= _nd
        else:
            return self._build_date(year, self._month, self._day, self._leap, self._reverse)

    def _resolve_monthly(self, year, month, leap=0) -> List[Union[date, LunarDate]]:
        month_meta = LCalendars.iter_year_month(year)
        if month == 0:
            data = []
            for _m, _nd, _l in month_meta:
                if self._reverse == 0:
                    day = self._day
                else:
                    day = LCalendars.ndays(year, _m, _l) - self._day + 1
                data.append(LunarDate(year, _m, day, _l))
            return data
        else:
            return self._build_date(year, month, self._day, leap, self._reverse)

    def _build_date(self, year, month, day, leap, reverse):
        if leap not in (0, 1):
            leaps = (0, 1)
        else:
            leaps = (leap,)
        data_tuples = []
        for v_leap in leaps:
            if v_leap == 1 and LCalendars.leap_month(year) != month:
                continue
            if reverse:
                v_day = LCalendars.ndays(year, month, v_leap) - day + 1
            else:
                v_day = day
            data_tuples.append(LunarDate(year, month, v_day, v_leap))
        return data_tuples
