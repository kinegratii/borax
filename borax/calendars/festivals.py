# coding=utf8
import csv
from collections import defaultdict
from pathlib import Path
import calendar
import re
from datetime import date
from typing import Union, List, Iterator, Tuple

from borax.calendars.lunardate import LunarDate, LCalendars

MDate = Union[date, LunarDate]


def date2mixed(date_obj):
    if isinstance(date_obj, date):
        return date_obj.strftime('0%Y%m%d0')
    elif isinstance(date_obj, LunarDate):
        return date_obj.strftime('1%y%A%B%l')
    else:
        raise TypeError('Unsupported type: {}'.format(date_obj.__class__.__name__))


def mixed2date(src):
    ds = DateSchemaFactory.from_string(src)
    return ds.resolve()


class DateSchema:
    date_class = None

    def __init__(self, *args, **kwargs):
        """Any subclass MUST call this initial in its own initial.
        """
        self._ignore_year = kwargs.get('ignore_year', True)
        self._schema = kwargs.get('schema', None)
        self.name = kwargs.get('name')
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def fuzzy(self):
        return self.year == 0

    # --------------------------  API  -----------------------------------

    def match(self, date_obj: MDate) -> bool:
        date_obj = self._normalize(date_obj)
        return (self.resolve(date_obj.year) - date_obj).days == 0

    def countdown(self, date_obj: MDate = None) -> int:
        if date_obj is None:
            date_obj = self.date_class.today()
        return self._countdown(self._normalize(date_obj))

    def resolve(self, year=0):
        year = year or self.year
        if year:
            return self._resolve(year)
        raise ValueError('Unable resolve the date without a specified year.')

    # --------------------  Internal Methods  -------------------------------

    def _normalize(self, date_obj):
        date_class = self._get_date_class()
        if not isinstance(date_obj, (date, LunarDate)):
            raise TypeError('Unsupported type: {}'.format(date_obj.__class__.__name__))
        if isinstance(date_obj, date_class):
            return date_obj
        if isinstance(date_class, date):
            return date_obj.to_solar_date()
        else:
            return LunarDate.from_solar(date_obj)

    # Interfaces in the subclasses

    def _get_date_class(self):
        return self.date_class

    def _resolve(self, year):
        raise NotImplementedError('Any subclass MUST overwrite this method.')

    def _countdown(self, date_obj):
        date_obj = self._normalize(date_obj)
        d = self.resolve(date_obj.year)
        offset = (d - date_obj).days
        if offset < 0:
            d = self._resolve(date_obj.year + 1)
        return (d - date_obj).days


class SolarSchema(DateSchema):
    date_class = date

    def __init__(self, month, day, year=0, reverse=0, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self._reverse = reverse
        super().__init__(**kwargs)

    def _resolve(self, year):
        if self._reverse == 0:
            day = self.day
        else:
            day = calendar.monthrange(self.year, self.month)[1] - self.day + 1
        return date(year, self.month, day)


class LunarSchema(DateSchema):
    date_class = LunarDate

    def __init__(self, month, day, year=0, leap=0, ignore_leap=1, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.leap = leap
        self._ignore_leap = ignore_leap
        super().__init__(**kwargs)

    def match(self, date_obj):
        date_obj = self._normalize(date_obj)
        if self._ignore_leap and date_obj.leap == 1:
            date_obj = date_obj.replace(leap=0)
        return super().match(date_obj)

    def _resolve(self, year):
        return LunarDate(year, self.month, self.day, self.leap)


class WeekSchema(DateSchema):
    date_class = date

    def __init__(self, year, month, index, week, **kwargs):
        self.year = year
        self.month = month
        self.index = index
        self.week = week
        super().__init__(**kwargs)

    def _resolve(self, year):
        day = WeekSchema.week_day(year, self.month, self.index, self.week)
        return date(year, self.month, day)

    @staticmethod
    def week_day(year: int, month: int, index: int, week: int) -> int:
        i = 0
        cal = calendar.Calendar()
        for d, w in cal.itermonthdays2(year, month):
            if d != 0 and w == week:
                i += 1
                if i == index:
                    return d

    def __hash__(self):
        return hash((self.year, self.month, self.index, self.week))


class DayLunarSchema(DateSchema):
    date_class = LunarDate

    def __init__(self, month, day, year=0, reverse=0, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self._reverse = reverse
        super().__init__(**kwargs)

    def _resolve(self, year):
        if self._reverse == 0:
            day = self.day
        else:
            day = LCalendars.ndays(year, self.month) - self.day + 1
        return LunarDate(year, self.month, day)


class TermSchema(DateSchema):
    date_class = date

    def __init__(self, index, year=None, **kwargs):
        self.year = year
        self.index = index
        super().__init__(**kwargs)

    def _resolve(self, year):
        return LCalendars.create_solar_date(year, term_index=self.index)


class DateSchemaFactory:
    LOOKUP = [
        # 公历
        [re.compile(r'^(?P<schema>0)(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<reverse>[01])$'), SolarSchema],
        # 农历
        [re.compile(r'^(?P<schema>1)(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<leap>[01])$'), LunarSchema],
        [re.compile(r'^(?P<schema>2)(?P<year>\d{4})(?P<month>\d{2})(?P<index>\d{2})(?P<week>[0-6])$'), WeekSchema],
        [re.compile(r'^(?P<schema>3)(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<reverse>[01])$'), DayLunarSchema],
        [re.compile(r'^(?P<schema>4)(?P<year>\d{4})00(?P<index>\d{2})0$'), TermSchema],
    ]

    @staticmethod
    def from_string(src: str, **kwargs) -> DateSchema:
        for regex, cls in DateSchemaFactory.LOOKUP:
            m = regex.match(src)
            if m:
                kw = {k: int(v) for k, v in m.groupdict().items()}
                return cls(**kw, **kwargs)
        else:
            raise ValueError('Unable to match any schema for {}'.format(src))


# -------------------- Festival Dataset  ---------------------------------
def read_dataset():
    field_names = ['src', 'name']
    data_file = Path(__file__).parent / 'FestivalData.txt'
    with data_file.open(encoding='utf8') as f:
        reader = csv.DictReader(f, fieldnames=field_names)
        for row in reader:
            try:
                yield DateSchemaFactory.from_string(src=row['src'], name=row['name'])
            except ValueError:
                continue


def get_festival(name: str) -> DateSchema:
    for schema in read_dataset():
        if schema.name == name:
            return schema


def iter_festival_countdown(countdown: int, date_obj: MDate = None) -> Iterator[Tuple[int, List]]:
    """Return countdown of festivals.
    """
    festival_names = defaultdict(list)
    for schema in read_dataset():
        _offset = schema.countdown(date_obj)
        if _offset <= countdown:
            festival_names[_offset].append(schema.name)
    for offset in sorted(festival_names.keys()):
        yield offset, festival_names[offset]
