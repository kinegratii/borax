# coding=utf-8

import calendar
import enum
from datetime import date, timedelta
from typing import Union, List, Tuple, Optional

from borax.calendars.lunardate import LunarDate, LCalendars, TERMS_CN

__all__ = [
    'SolarFestival', 'LunarFestival', 'WeekFestival', 'TermFestival', 'Period', 'decode', 'FestivalError',
    'YEARLY', 'MONTHLY'
]

MixedDate = Union[date, LunarDate]

(YEARLY, MONTHLY) = list(range(2))

# Private Global Variables

_IGNORE_LEAP_MONTH = 3


class Flag:
    LEAP_MONTH = 1
    REVERSE = 2
    MONTHLY = 4
    DAY_YEAR_ORDER = 8


class FestivalSchema(enum.IntEnum):
    SOLAR = 0
    LUNAR = 1
    WEEK = 2
    LUNAR_OLD = 3  # 兼容旧版本
    TERM = 4


class GeneralDate:
    __slots__ = ['solar', 'lunar']

    def __init__(self, date_obj: MixedDate):
        self.solar = LCalendars.cast_date(date_obj, date)
        self.lunar = LCalendars.cast_date(date_obj, LunarDate)


class Period:
    @staticmethod
    def solar_year(year):
        return date(year, 1, 1), date(year, 12, 31)

    @staticmethod
    def solar_month(year, month):
        ndays = calendar.monthrange(year, month)[1]
        return date(year, month, 1), date(year, month, ndays)

    @staticmethod
    def lunar_year(year):
        return LunarDate(year, 1, 1), LunarDate(year + 1, 1, 1) - timedelta(days=1)

    @staticmethod
    def lunar_month(year, month, leap=_IGNORE_LEAP_MONTH):
        has_leap = LCalendars.leap_month(year) == month
        if has_leap:
            if leap == _IGNORE_LEAP_MONTH:
                sl, el = 0, 1
            else:
                sl, el = leap, leap
        else:
            sl, el = 0, 0
        ndays = LCalendars.ndays(year, month, el)
        return LunarDate(year, month, 1, sl), LunarDate(year, month, ndays, el)


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

    @property
    def name(self):
        return self._name

    def is_(self, date_obj: MixedDate) -> bool:
        date_obj = self._normalize(date_obj)
        try:
            date_list = self._resolve(date_obj.year, date_obj.month)
            for day in date_list:
                if (day - date_obj).days == 0:
                    return True
            else:
                return False
        except FestivalError:
            return False

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

    def _resolve(self, year: int, month: int = 0, leap=_IGNORE_LEAP_MONTH) -> List[Union[date, LunarDate]]:
        _y = year
        if month != 0 and self._month != 0 and month != self._month:
            raise FestivalError('DateDoesNotExist', 'Date does not exist.')
        if self._freq == MONTHLY and self._month == 0:
            _m = month
        else:
            _m = self._month

        try:
            if self._freq == YEARLY:
                date_list = self._resolve_yearly(_y)
            else:
                date_list = self._resolve_monthly(_y, _m, leap)
        except FestivalError:
            raise
        if month != 0:
            new_date_list = []
            for date_obj in date_list:
                is_match = (year, month) == (date_obj.year, date_obj.month) and (
                        self.date_class == date or leap == _IGNORE_LEAP_MONTH or leap == date_obj.leap)
                if is_match:
                    new_date_list.append(date_obj)
            return new_date_list
        else:
            return date_list

    def list_days(self, start_date=None, end_date=None, reverse=False):
        """
        Festival.list_days(*Period.solar_year(2021))

        :param start_date:
        :param end_date:
        :param reverse:
        :return:
        """
        if start_date is None:
            start_date = LunarDate.min
        start_date = self._normalize(start_date)
        if end_date is None:
            end_date = LunarDate.max
        end_date = self._normalize(end_date)
        if self._freq == YEARLY:
            for day in self._list_yearly(start_date, end_date, reverse):
                if start_date <= day <= end_date:
                    yield day
        else:
            for day in self._list_monthly(start_date, end_date, reverse):
                if start_date <= day <= end_date:
                    yield day

    def countdown(self, date_obj: MixedDate = None) -> Tuple[int, Optional[GeneralDate]]:
        if date_obj is None:
            date_obj = date.today()
        days = list(self.list_days(start_date=date_obj))
        if len(days):
            this_day = days[0]
            return LCalendars.delta(this_day, date_obj), GeneralDate(this_day)
        return -1, None

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
        sy, sm = start_date.year, start_date.month
        ey, em = end_date.year, end_date.month

        for year, month in self._iter_solar_month(sy, sm, ey, em, reverse):
            try:
                obj_list = self._resolve(year, month)
                for day in obj_list:
                    yield day
            except FestivalError:
                continue

    def _iter_solar_month(self, sy, sm, ey, em, reverse=False):
        if reverse:
            ym_start = 12 * sy + sm - 1
            ym_end = 12 * ey + em - 1
            for ym in range(ym_end, ym_start - 1, -1):
                y, m = divmod(ym, 12)
                yield y, m + 1
        else:
            ym_start = 12 * sy + sm - 1
            ym_end = 12 * ey + em - 1
            for ym in range(ym_start, ym_end + 1):
                y, m = divmod(ym, 12)
                yield y, m + 1

    def _normalize(self, date_obj):
        date_class = self.date_class
        return LCalendars.cast_date(date_obj, date_class)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        return []

    def _resolve_monthly(self, year, month, leap=0) -> List[Union[date, LunarDate]]:
        return []

    def encode(self) -> str:
        pass


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
                day = calendar.monthrange(year, month)[1] - self._day + 1
            return [date(year, month, day)]

    def encode(self) -> str:
        flag = 0
        if self._reverse == 1:
            flag += Flag.REVERSE
        if self._freq == MONTHLY:
            flag += Flag.MONTHLY
        if self._month == 0:
            flag += Flag.DAY_YEAR_ORDER
        if self._month != 0:
            return '0{:02d}{:02d}{:X}'.format(self._month, self._day, flag)
        else:
            return '0{:04d}{:X}'.format(self._day, flag)


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

    def encode(self) -> str:
        return '2{:02d}{:02d}{}'.format(self._month, self._week_index, self._week_no)


class TermFestival(Festival):
    date_class = date

    def __init__(self, *, index=None, name=None):
        if index is None:
            index = TERMS_CN.index(name)
        super().__init__(freq=YEARLY, name=name, index=index)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        return [LCalendars.create_solar_date(year, term_index=self._term_index, term_name=self._name)]

    def encode(self) -> str:
        return '400{:02d}0'.format(self._term_index)


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
        month_meta = list(LCalendars.iter_year_month(year))

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
                data.extend(self._build_date(year, _m, self._day, _l, self._reverse))
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

    def _list_monthly(self, start_date, end_date, reverse):
        sy, sm, sl = start_date.year, start_date.month, start_date.leap
        ey, em, el = end_date.year, end_date.month, end_date.leap

        for year, month, leap in self._iter_lunar_month(sy, sm, sl, ey, em, el, reverse):
            try:
                obj_list = self._resolve(year, month, leap)
                for day in obj_list:
                    yield day
            except FestivalError:
                continue

    def _iter_lunar_month(self, sy, sm, sl, ey, em, el, reverse=False):
        if reverse:
            for year in range(ey, sy - 1, -1):
                ym = list(LCalendars.iter_year_month(year))[::-1]
                for month, _, leap in ym:
                    if self._leap != _IGNORE_LEAP_MONTH and self._leap != leap:
                        continue
                    if (sy, sm, sl) <= (year, month, leap) <= (ey, em, el):
                        yield year, month, leap
        else:
            for year in range(sy, ey + 1):
                for month, _, leap in LCalendars.iter_year_month(year):
                    if self._leap != _IGNORE_LEAP_MONTH and self._leap != leap:
                        continue
                    if (sy, sm, sl) <= (year, month, leap) <= (ey, em, el):
                        yield year, month, leap

    def encode(self) -> str:
        flag = 0
        if self._reverse == 1:
            flag += Flag.REVERSE
        if self._freq == MONTHLY:
            flag += Flag.MONTHLY
        if self._leap == 1:
            flag += Flag.LEAP_MONTH
        if self._month == 0:
            flag += Flag.DAY_YEAR_ORDER
        if self._month != 0:
            return '1{:02d}{:02d}{:X}'.format(self._month, self._day, flag)
        else:
            return '1{:04d}{:X}'.format(self._day, flag)


__SCHEMA_CLASS_DICT = {
    FestivalSchema.SOLAR: SolarFestival,
    FestivalSchema.LUNAR: LunarFestival,
    FestivalSchema.WEEK: WeekFestival,
    FestivalSchema.TERM: TermFestival
}


def decode(raw: str) -> Festival:
    if not raw[:-1].isdigit() or raw[-1] not in '0123456789ABCDEF':
        raise ValueError('Invalid raw:{}'.format(raw))
    if len(raw) == 10:
        schema, month, day, flag = int(raw[0]), int(raw[5:7]), int(raw[7:9]), int(raw[9], 16)
    elif len(raw) == 6:
        schema, month, day, flag = int(raw[0]), int(raw[1:3]), int(raw[3:5]), int(raw[5], 16)
    else:
        raise ValueError('Invalid length.')
    if schema == FestivalSchema.LUNAR_OLD:
        if flag == 1:
            schema, flag = FestivalSchema.LUNAR, 2
        else:
            schema, flag = FestivalSchema.LUNAR, 0

    if schema not in __SCHEMA_CLASS_DICT:
        raise ValueError('Invalid schema: {}'.format(schema))
    cls = __SCHEMA_CLASS_DICT[schema]

    attrs = {}
    if schema in [FestivalSchema.SOLAR, FestivalSchema.LUNAR]:

        is_day_of_year, is_month, is_reverse, is_leap = (
            flag & Flag.DAY_YEAR_ORDER == Flag.DAY_YEAR_ORDER,
            flag & Flag.MONTHLY == Flag.MONTHLY,
            flag & Flag.REVERSE == Flag.REVERSE,
            flag & Flag.LEAP_MONTH == Flag.LEAP_MONTH
        )
        if is_month:
            attrs['freq'] = MONTHLY
        else:
            attrs['freq'] = YEARLY
        if is_leap:
            attrs['leap'] = 1
        else:
            attrs['leap'] = _IGNORE_LEAP_MONTH
        if is_day_of_year:
            day = month * 100 + day
            month = 0
        if is_reverse:
            day = -day
        attrs['month'] = month
        attrs['day'] = day
        if schema == FestivalSchema.SOLAR:
            del attrs['leap']
    elif schema == FestivalSchema.WEEK:
        attrs['month'] = month
        attrs['index'] = day
        attrs['week'] = flag
    elif schema == FestivalSchema.TERM:
        attrs['index'] = day
    return cls(**attrs)
