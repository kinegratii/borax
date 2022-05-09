# coding=utf-8

import calendar
import collections
import csv
import enum
from datetime import date, timedelta
from pathlib import Path
from typing import List, Tuple, Optional, Union, Iterator, Set, Generator

from borax.calendars.lunardate import LunarDate, LCalendars, TermUtils, TextUtils

__all__ = [
    'FestivalError', 'WrappedDate', 'Period',
    'FreqConst',
    'SolarFestival', 'LunarFestival', 'WeekFestival', 'TermFestival',
    'encode', 'decode', 'decode_festival',
    'FestivalLibrary',
]

MixedDate = Union[date, LunarDate]


class FreqConst:
    YEARLY = 0
    MONTHLY = 1


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


class FestivalCatalog:
    birthday = 'birthday'
    foundation = 'foundation'
    public = 'public'
    tradition = 'tradition'
    term = 'term'
    other = 'other'


class WrappedDate:
    """A date object with solar and lunar calendars."""
    __slots__ = ['solar', 'lunar', 'name', '_fl']

    def __init__(self, date_obj: MixedDate, name: str = ''):
        self.solar = LCalendars.cast_date(date_obj, date)
        self.lunar = LCalendars.cast_date(date_obj, LunarDate)
        self.name = name
        if isinstance(date_obj, date):
            self._fl = 's'
        else:
            self._fl = 'l'

    def __iter__(self):
        yield self.solar
        yield self.lunar

    def __str__(self):
        return '{}({})'.format(self.solar, self.lunar.cn_str())

    def __repr__(self):
        return '<WrappedDate:{}>'.format(self.__str__())

    def __add__(self, other):
        if isinstance(other, timedelta):
            return WrappedDate(self.solar + other)
        raise TypeError

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        """This is the basic method for comparable feature.
        :param other: a instance of LunarDate / date / timedelta
        :return:
        """
        if isinstance(other, LunarDate):
            return self.solar - other.to_solar_date()
        elif isinstance(other, date):
            return self.solar - other
        elif isinstance(other, timedelta):
            res = self.solar - other
            return WrappedDate(res)
        raise TypeError

    def __rsub__(self, other):
        if isinstance(other, date):
            return other - self.solar
        raise TypeError

    def __key(self):
        return self.solar.year, self.solar.month, self.solar.day

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__key() == other.__key()

    def __getstate__(self):
        return self.__key()

    def __setstate__(self, state):
        _year, _month, _day = state
        self.solar = date(_year, _month, _day)

    def simple_str(self):
        """Display as solar and lunar.

        Example:
            >>>WrappedDate(LunarDate(2022, 3, 4))
            '2022-04-04(三月初四)'
        """
        return f'{self.solar}({self.lunar:%c})'

    def encode(self) -> str:
        if self._fl == 'l':
            festival = LunarFestival(month=self.lunar.month, day=self.lunar.day, leap=self.lunar.leap)
            encoded_str = festival.encode()
            return '{}{:04d}{}'.format(encoded_str[0], self.lunar.year, encoded_str[1:])
        else:
            festival = SolarFestival(month=self.solar.month, day=self.solar.day)
            encoded_str = festival.encode()
            return '{}{:04d}{}'.format(encoded_str[0], self.solar.year, encoded_str[1:])

    @classmethod
    def decode(cls, raw: str) -> 'WrappedDate':
        return decode(raw)


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
    """A object standard for a festival."""
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

        self._cyear = 0
        self._tmp = {}
        self._catalog = kwargs.get('catalog')

    def gets(self, *args):
        def _get(_f):
            return getattr(self, '_' + _f)

        values = list(map(_get, args))
        if len(args) == 1:
            return values[0]
        return values

    def set_name(self, name):
        self._name = name
        return self

    @property
    def cyear(self):
        return self._cyear

    @cyear.setter
    def cyear(self, value):
        self._cyear = value

    @property
    def name(self):
        return self._name

    def _get_description(self) -> str:
        pass

    @property
    def description(self) -> str:
        return self._get_description()

    @property
    def catalog(self) -> str:
        return self._catalog

    @catalog.setter
    def catalog(self, catalog: str):
        self._catalog = catalog

    def __str__(self):
        return '{} {}'.format(self.name, self.description)

    def __repr__(self):
        return '<{} {} {}>'.format(self.__class__.__name__, self.name, self.description)

    def __eq__(self, other):
        return isinstance(self, type(other)) and other.name == self.name

    def is_(self, date_obj: MixedDate) -> bool:
        date_obj = self._normalize(date_obj)
        try:
            date_list = self._resolve(date_obj.year, date_obj.month)
            for day in date_list:
                if (day - date_obj).days == 0:
                    return True
            return False
        except FestivalError:
            return False

    def at(self, year: int, month: int = 0, leap=0) -> MixedDate:
        date_list = self._resolve(year, month, leap)
        if len(date_list) == 0:
            raise FestivalError('DateDoesNotExit', 'The date does not exist.')
        if len(date_list) > 1:
            raise FestivalError('MultipleDateExist', 'The result return {} dates.'.format(len(date_list)))
        return date_list[0]

    def _resolve(self, year: int, month: int = 0, leap=_IGNORE_LEAP_MONTH) -> List[Union[date, LunarDate]]:
        _y = year
        if month != 0 and self._month != 0 and month != self._month:
            raise FestivalError('DateDoesNotExist', 'Date does not exist.')
        if self._freq == FreqConst.MONTHLY and self._month == 0:
            _m = month
        else:
            _m = self._month

        if self._freq == FreqConst.YEARLY:
            date_list = self._resolve_yearly(_y)
        else:
            date_list = self._resolve_monthly(_y, _m, leap)
        if month != 0:
            new_date_list = []
            for date_obj in date_list:
                is_match = (year, month) == (date_obj.year, date_obj.month)
                is_match = is_match and (self.date_class == date or leap == _IGNORE_LEAP_MONTH or leap == date_obj.leap)
                if is_match:
                    new_date_list.append(date_obj)
            return new_date_list
        else:
            return date_list

    def iter_days(self, start_date=None, end_date=None, reverse=False) -> Iterator[WrappedDate]:

        if start_date is None:
            start_date = LunarDate.min
        start_date = self._normalize(start_date)
        if end_date is None:
            end_date = LunarDate.max
        end_date = self._normalize(end_date)
        if self._freq == FreqConst.YEARLY:
            for day in self._list_yearly(start_date, end_date, reverse):
                if start_date <= day <= end_date:
                    yield WrappedDate(day, name=self.name)
        else:
            for day in self._list_monthly(start_date, end_date, reverse):
                if start_date <= day <= end_date:
                    yield WrappedDate(day, name=self.name)

    def list_days(self, start_date=None, end_date=None, reverse: bool = False, count: int = -1) -> List[WrappedDate]:
        """Return the day list for this festival in day range [start_date, end_date].(Include start/end date)

        Example:
            Festival.list_days(start_date=date(2022, 1, 1))

            Festival.list_days(start_date=LunarDate.today(),count=10)

            Festival.list_days(*Period.solar_year(2021))
        """
        days_list = []
        ncount = 0
        for day in self.iter_days(start_date=start_date, end_date=end_date, reverse=reverse):
            if ncount == count:
                break
            days_list.append(day)
            ncount += 1
        return days_list

    def list_days_in_future(self, end_date=None, reverse: bool = False, count: int = -1) -> List[WrappedDate]:
        """Return the day list for this festival in future days."""
        return self.list_days(start_date=date.today(), end_date=end_date, reverse=reverse, count=count)

    def list_days_in_past(self, start_date=None, reverse: bool = False, count: int = -1) -> List[WrappedDate]:
        """Return the day list for this festival in past days."""
        return self.list_days(start_date=start_date, end_date=date.today(), reverse=reverse, count=count)

    def get_one_day(self, start_date=None, end_date=None) -> Optional[WrappedDate]:
        days = self.list_days(start_date, end_date, count=1)
        if days:
            return days[0]

    def countdown(self, date_obj: MixedDate = None) -> Tuple[int, Optional[WrappedDate]]:
        """Return the offset-date tuple of the first day for this festival in future days."""
        if date_obj is None:
            date_obj = date.today()
        days = list(self.list_days(start_date=date_obj))
        if days:
            this_day = days[0]
            return LCalendars.delta(this_day, date_obj), this_day
        return -1, None

    def _list_yearly(self, start_date, end_date, reverse):
        sy = start_date.year
        ey = end_date.year
        if reverse:
            my_iter = range(ey, sy - 1, -1)
        else:
            my_iter = range(sy, ey + 1)
        for year in my_iter:
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
        """A core method.
        A day list in the year when month=0.
        """
        return []

    def encode(self) -> str:
        pass


class SolarFestival(Festival):
    date_class = date

    def __init__(self, *, day, freq=FreqConst.YEARLY, month=0, name=None):
        if day < 0:
            day = -day
            reverse = 1
        else:
            reverse = 0
        super().__init__(name=name, freq=freq, month=month, day=day, reverse=reverse)

    def _get_description(self) -> str:
        cn_list = ['公历']
        day_order = False
        if self._freq == FreqConst.YEARLY:
            if self._month != 0:
                cn_list.append('每年{}月'.format(self._month))
            else:
                cn_list.append('每年')
                day_order = True
        else:
            cn_list.append('每月')
        if self._reverse:
            cn_list.append('倒数第{}天'.format(self._day))
        else:
            if day_order:
                cn_list.append('第{}天'.format(self._day))
            else:
                cn_list.append('{}日'.format(self._day))
        return ''.join(cn_list)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
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
        if self._freq == FreqConst.MONTHLY:
            flag += Flag.MONTHLY
        if self._month == 0:
            flag += Flag.DAY_YEAR_ORDER
        if self._month != 0:
            return '0{:02d}{:02d}{:X}'.format(self._month, self._day, flag)
        else:
            return '0{:04d}{:X}'.format(self._day, flag)


class WeekFestival(Festival):
    date_class = date

    def __init__(self, *, month, index, week, name=None, freq=FreqConst.YEARLY):
        if index < 0:
            index = -index
            reverse = 1
        else:
            reverse = 0
        if month > 0 and freq == FreqConst.MONTHLY:
            raise ValueError('freq must be FreqConst.YEARLY when month is not 0.')
        if month == 0:
            freq = FreqConst.MONTHLY
        super().__init__(name=name, freq=freq, month=month, index=index, week=week, reverse=reverse)

    def _get_description(self) -> str:
        index_str = '倒数' if self._reverse == 1 else ''
        month_str = f'{self._month}月' if self._month > 0 else '每月'
        return '公历{}{}第{}个星期{}'.format(month_str, index_str, self._week_index, '一二三四五六日'[self._week_no])

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        s_i = -self._week_index if self._reverse == 1 else self._week_index
        day = WeekFestival.week_day(year, self._month, s_i, self._week_no)
        return [date(year, self._month, day)]

    def _resolve_monthly(self, year, month, leap=0) -> List[Union[date, LunarDate]]:
        assert self._month == 0
        s_i = -self._week_index if self._reverse == 1 else self._week_index
        day_list = []
        for month in range(1, 13):
            try:
                day_no = WeekFestival.week_day(year, month, s_i, self._week_no)
                day_list.append(date(year, month, day_no))
            except FestivalError:
                pass
        return day_list

    @staticmethod
    def week_day(year: int, month: int, index: int, week: int) -> int:
        w, ndays = calendar.monthrange(year, month)
        if week >= w:
            d0 = week - w + 1
        else:
            d0 = 8 - (w - week)

        ds = list(range(d0, ndays + 1, 7))
        ll = len(ds)
        if -ll <= index < 0:
            return ds[index]
        elif 0 < index <= ll:
            return ds[index - 1]
        else:
            raise FestivalError('InvalidIndex', f'Invalid index: {index}')

    def encode(self) -> str:
        return '2{:02d}{}{}{}'.format(self._month, self._reverse, self._week_index, self._week_no)


class TermFestival(Festival):
    date_class = date

    def __init__(self, *, index=None, name=None):
        if index is None:
            index = TermUtils.get_index_for_name(name)
        else:
            name = TermUtils.get_name_for_index(index)
        super().__init__(freq=FreqConst.YEARLY, name=name, index=index)

    def _get_description(self) -> str:
        return '公历每年{}节气'.format(self.name)

    def _resolve_yearly(self, year) -> List[Union[date, LunarDate]]:
        try:
            date_obj = TermUtils.nth_term_day(year, term_index=self._term_index, term_name=self._name)
            return [date_obj]
        except ValueError as e:
            if str(e).startswith('Invalid'):
                return []
            else:
                raise ValueError from e

    def encode(self) -> str:
        return '400{:02d}0'.format(self._term_index)


class LunarFestival(Festival):
    date_class = LunarDate

    def __init__(self, *, day, freq=FreqConst.YEARLY, month=0, leap=_IGNORE_LEAP_MONTH, name=None):
        if day < 0:
            day = -day
            reverse = 1
        else:
            reverse = 0
        super().__init__(freq=freq, name=name, month=month, day=day, leap=leap, reverse=reverse)

    def _get_description(self) -> str:
        cn_list = ['农历']
        day_order = False
        if self._freq == FreqConst.YEARLY:
            if self._month != 0:
                cn_list.append('每年{}月'.format(TextUtils.month_cn(self._month)))
            else:
                cn_list.append('每年')
                day_order = True
        else:
            cn_list.append('每月')
        if self._reverse:
            cn_list.append('倒数第{}天'.format(self._day))
        else:
            if day_order:
                cn_list.append('第{}天'.format(self._day))
            else:
                cn_list.append('{}'.format(TextUtils.day_cn(self._day)))
        return ''.join(cn_list)

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
        if self._freq == FreqConst.MONTHLY:
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


def encode(obj: Union[WrappedDate, Festival]) -> str:
    return obj.encode()


def decode_festival(raw: Union[str, bytes]) -> Festival:
    if isinstance(raw, bytes):
        raw = raw.decode()
    if not raw[:-1].isdigit() or raw[-1] not in '0123456789ABCDEF':
        raise ValueError('Invalid raw:{}'.format(raw))
    cyear = 0
    if len(raw) == 10:
        schema, month, day, flag = int(raw[0]), int(raw[5:7]), int(raw[7:9]), int(raw[9], 16)
        cyear = int(raw[1:5])
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
            attrs['freq'] = FreqConst.MONTHLY
        else:
            attrs['freq'] = FreqConst.YEARLY
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
        if day > 10:
            attrs['index'] = -(day % 10)
        else:
            attrs['index'] = day
        attrs['week'] = flag
    elif schema == FestivalSchema.TERM:
        attrs['index'] = day
    obj = cls(**attrs)
    if cyear:
        obj.cyear = cyear
    return obj


def decode(raw: Union[str, bytes]) -> Union[WrappedDate, Festival]:
    if isinstance(raw, bytes):
        raw = raw.decode()
    festival = decode_festival(raw)
    if festival.cyear == 0:
        return festival
    if isinstance(festival, SolarFestival):
        year, month, day = festival.gets('cyear', 'month', 'day')
        return WrappedDate(date(year, month, day))
    elif isinstance(festival, LunarFestival):
        if festival.gets('leap') == 1:
            leap = 1
        else:
            leap = 0
        year, month, day = festival.gets('cyear', 'month', 'day')
        return WrappedDate(LunarDate(year, month, day, leap))
    else:
        raise FestivalError('Invalid FestivalSchema', '')


class FestivalLibrary(collections.UserList):
    """A festival collection."""

    def get_code_set(self) -> Set[str]:
        """Get codes for all festivals.
        """
        return set([f.encode() for f in self.data])

    def extend_unique(self, other):
        """Add a new festival if code does not exist.
        """
        f_codes = set({f.encode() for f in self.data})
        if isinstance(other, collections.UserList):
            new_data = other.data
        else:
            new_data = other
        for item in new_data:
            if isinstance(item, Festival):
                if item.encode() not in f_codes:
                    self.data.append(item)
            elif isinstance(item, str):
                try:
                    festival = decode_festival(item)
                    if item not in f_codes:
                        self.data.append(festival)
                except ValueError:
                    pass
        return self

    def get_festival(self, name: str) -> Optional[Festival]:
        """Get a Festival object by the name."""
        for festival in self:
            if festival.name == name:
                return festival
        return None

    def get_festival_names(self, date_obj: MixedDate) -> list:
        """Get name list for a date object."""
        names = []
        for festival in self:
            if festival.is_(date_obj):
                names.append(festival.name)
        return names

    def iter_festival_countdown(
            self, countdown: Optional[int] = None, date_obj: MixedDate = None
    ) -> Generator[Tuple[int, List], None, None]:
        ndays2festivals = collections.defaultdict(list)
        for festival in self:
            ndays, gd = festival.countdown(date_obj)
            if countdown is None or ndays <= countdown:
                ndays2festivals[ndays].append(gd)
        for offset in sorted(ndays2festivals.keys()):
            yield offset, ndays2festivals[offset]

    def iter_month_daytuples(self, year: int, month: int, firstweekday: int = 0, return_pos: bool = False):
        """迭代返回公历月份（含前后完整日期）中每个日期信息
        """
        row = 0
        cal = calendar.Calendar(firstweekday=firstweekday)
        for days in cal.monthdayscalendar(year, month):
            for col, day in enumerate(days):
                if day == 0:
                    text = ''
                    wd = None
                else:
                    ld = LunarDate.from_solar_date(year, month, day)
                    text = ''
                    names = self.get_festival_names(ld)
                    if names:
                        text = names[0]
                    if ld.term and not text:
                        text = ld.term
                    elif not text:
                        text = ld.cn_day_calendar
                    wd = WrappedDate(ld)
                if return_pos:
                    yield day, text, wd, row, col
                else:
                    yield day, text, wd
            row += 1

    def monthdaycalendar(self, year: int, month: int, firstweekday: int = 0):
        """返回二维列表，每一行表示一个星期。逻辑同iter_month_daytuples。
        :param year:
        :param month:
        :param firstweekday:
        :return:
        """
        days = list(self.iter_month_daytuples(year, month, firstweekday))
        return [days[i:i + 7] for i in range(0, len(days), 7)]

    def to_csv(self, path_or_buf):
        if isinstance(path_or_buf, str):
            fileobj = open(path_or_buf, 'w', encoding='utf8', newline='')
        elif isinstance(path_or_buf, Path):
            fileobj = path_or_buf.open('w', encoding='utf8', newline='')
        else:
            fileobj = path_or_buf
        writer = csv.writer(fileobj, )
        for festival in self:
            row = (festival.encode(), festival.name, festival.catalog)
            writer.writerow(row)

    @classmethod
    def load_file(cls, file_path: Union[str, Path], unique: bool = False) -> 'FestivalLibrary':
        if isinstance(file_path, str):
            file_path = Path(file_path)
        fl = cls()
        field_names = ['raw', 'name', 'catalog']
        with file_path.open(encoding='utf8') as f:
            reader = csv.DictReader(f, fieldnames=field_names)
            code_set = fl.get_code_set()
            # FIXME 多个节日在同一天的情况
            for row in reader:
                code = row['raw']
                if unique and code in code_set:
                    continue
                code_set.add(code)
                try:
                    festival = decode_festival(row['raw'])
                    festival.set_name(row['name'])
                    festival.catalog = row.get('catalog')
                    fl.append(festival)
                except ValueError as e:
                    print(e)
                    continue
        fl.sort(key=lambda x: x.encode())
        return fl

    def load_term_festivals(self):
        """Add 24-term festivals."""
        return self.extend_unique(['400{:02d}0'.format(i) for i in range(24)])

    @classmethod
    def load_builtin(cls, identifier: str = 'zh-Hans') -> 'FestivalLibrary':
        """Load builtin library in borax project."""
        file_dict = {
            'zh-Hans': 'FestivalData.csv',
            'ext1': 'dataset/festivals_ext1.csv'
        }
        file_path = Path(__file__).parent / file_dict.get(identifier)
        return cls.load_file(file_path)
