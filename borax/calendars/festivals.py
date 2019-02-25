# coding=utf8
import calendar
import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Union, List, Iterator, Tuple, Optional

from borax.calendars.lunardate import LunarDate, LCalendars, TERMS_CN

MDate = Union[date, LunarDate]
FestivalCountdownIterable = Iterator[Tuple[int, List]]

# Const values for date schema parameters
YEAR_ANY = 0


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


# -------- Schema Meta --------

class Field:
    def __init__(self, name=None, length=None, required=True):
        # length -> digit
        self.name = name
        self.length = length
        if self.name:
            self.fmt = '{' + '0' + ':0' + str(length) + 'd}'
            self.value = None
        else:
            self.fmt = None
            self.value = '0' * length
        self.required = required

    def resolve(self, value=None, short=False):
        if self.name:
            if short and not self.required:
                return ''  # Short Field
            else:
                return self.fmt.format(value)  # Full Field
        else:
            return self.value  # Const

    def __str__(self):
        if self.name:
            return '<Field:{}>'.format(self.name)
        else:
            return '<Const:{}>'.format(self.value)


f_schema = Field(name='schema', length=1)
f_year = Field(name='year', length=4, required=False)
f_month = Field(name='month', length=2)
f_day = Field(name='day', length=2)
f_reverse = Field(name='reverse', length=1)
f_index = Field(name='index', length=2)


class SchemaMixin:
    fields = []

    @classmethod
    def decode(cls, raw, short=False):
        i = 0
        data = {}
        for field in cls.fields:
            if short and not field.required:
                continue
            if field.name:
                data[field.name] = int(raw[i:i + field.length])
            i += field.length
        return cls(**data)

    def encode(self, short=False):
        ds = []
        for field in self.fields:
            if field.name:
                value = getattr(self, field.name)
            else:
                value = None
            ds.append(field.resolve(value, short))
        return ''.join(ds)


class DateSchema(SchemaMixin):
    date_class = None

    def __init__(self, *args, **kwargs):
        """Any subclass MUST call this initial in its own initial.
        """
        self._ignore_year = kwargs.get('ignore_year', True)
        self._schema = kwargs.get('schema', None)
        self.name = kwargs.get('name')
        self.raw = kwargs.get('raw')
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def fuzzy(self):
        return self.year == YEAR_ANY

    def __key(self):
        return list(map(int, self.encode()))

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.__key() == other.__key()

    # --------------------------  API  -----------------------------------

    def match(self, date_obj: MDate) -> bool:
        date_obj = self._normalize(date_obj)
        return (self.resolve(date_obj.year) - date_obj).days == 0

    def delta(self, date_obj: Optional[MDate] = None) -> int:
        if date_obj is None:
            date_obj = self._get_date_class().today()
        date_obj = self._normalize(date_obj)
        return (self.resolve(date_obj.year) - date_obj).days

    def countdown(self, date_obj: Optional[MDate] = None) -> int:
        if date_obj is None:
            date_obj = self.date_class.today()
        return self._countdown(self._normalize(date_obj))

    def resolve(self, year: int = YEAR_ANY) -> MDate:
        """Return the date object in the solar / lunar year.
        :param year:
        :return:
        """
        year = year or self.year
        if year:
            return self._resolve(year)
        raise ValueError('Unable resolve the date without a specified year.')

    def resolve_solar(self, year: int) -> date:
        """Return the date object in a solar year.
        :param year:
        :return:
        """
        if self.date_class == date:
            return self.resolve(year)
        else:
            solar_date = LCalendars.cast_date(self.resolve(year), date)
            offset = solar_date.year - year
            if offset:
                solar_date = LCalendars.cast_date(self.resolve(year - offset), date)
            return solar_date

    # --------------------  Internal Methods  -------------------------------

    def _normalize(self, date_obj):
        date_class = self._get_date_class()
        return LCalendars.cast_date(date_obj, date_class)

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
    fields = [f_schema, f_year, f_month, f_day, f_reverse]

    def __init__(self, month, day, year=YEAR_ANY, reverse=0, **kwargs):
        self.year = year
        self.month = month
        self.day = day
        self.reverse = reverse
        super().__init__(**kwargs)

    def _resolve(self, year):

        if self.reverse == 0:
            day = self.day
        else:
            day = calendar.monthrange(year, self.month)[1] - self.day + 1
        return date(year, self.month, day)


class LunarSchema(DateSchema):
    date_class = LunarDate
    fields = [f_schema, f_year, f_month, f_day, Field(name='leap', length=1)]

    def __init__(self, month, day, year=YEAR_ANY, leap=0, ignore_leap=1, **kwargs):
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
    fields = [f_schema, f_year, f_month, f_index, Field(name='week', length=1)]

    def __init__(self, month, index, week, year=YEAR_ANY, **kwargs):
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
    fields = [f_schema, f_year, f_month, f_day, f_reverse]

    def __init__(self, month, day, year=YEAR_ANY, reverse=0, **kwargs):
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
    fields = [f_year, Field(name=None, length=2), f_index, Field(name=None, length=1)]

    def __init__(self, index, year=YEAR_ANY, **kwargs):
        self.year = year
        self.index = index
        super().__init__(**kwargs)

    def _resolve(self, year):
        return LCalendars.create_solar_date(year, term_index=self.index)


class DateSchemaFactory:
    schema_dict = {
        0: SolarSchema,
        1: LunarSchema,
        2: WeekSchema,
        3: DayLunarSchema,
        4: TermSchema
    }

    @classmethod
    def from_string(cls, raw, **kwargs):
        lg = len(raw)
        if lg == 10:
            short = False
        elif lg == 6:
            short = True
        else:
            raise ValueError('Invalid length')
        schema_code = int(raw[0])
        schema_class = cls.schema_dict.get(schema_code)
        schema = schema_class.decode(raw, short)
        for k, v in kwargs.items():
            setattr(schema, k, v)
        return schema


# -------------------- Festival Dataset  ---------------------------------
LANG_FILES = {
    'zh-Hans': 'FestivalData.txt'
}


class FestivalFactory:
    """A container including a collection of festivals group by language or file.
    """

    def __init__(self, *, lang=None, file_path=None):
        if lang:
            file_path = Path(__file__).parent / LANG_FILES.get(lang)
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if file_path:
            self._schema_list = list(read_dataset(file_path))
        else:
            self._schema_list = []

    def add_festivals(self, festivals):
        self._schema_list.extend(festivals)

    def iter_festivals(self):
        for festival in self._schema_list:
            yield festival

    def get_festival(self, name: str) -> DateSchema:
        for schema in self._schema_list:
            if schema.name == name:
                return schema

    def iter_festival_countdown(self, countdown: Optional[int] = None,
                                date_obj: MDate = None) -> FestivalCountdownIterable:
        festival_names = defaultdict(list)
        for schema in self._schema_list:
            _offset = schema.countdown(date_obj)
            if countdown is None or _offset <= countdown:
                festival_names[_offset].append(schema.name)
        for offset in sorted(festival_names.keys()):
            yield offset, festival_names[offset]


def read_dataset(file_path=None):
    field_names = ['src', 'name']
    with file_path.open(encoding='utf8') as f:
        reader = csv.DictReader(f, fieldnames=field_names)
        for row in reader:
            try:
                yield DateSchemaFactory.from_string(raw=row['src'], name=row['name'])
            except ValueError:
                continue


# ---------- Shortcuts Method ----------

def get_festival(name: str, lang: str = 'zh-Hans') -> DateSchema:
    factory = FestivalFactory(lang=lang)
    return factory.get_festival(name)


def get_term(name: str) -> TermSchema:
    index = TERMS_CN.index(name)
    return TermSchema(index)


def iter_festival_countdown(countdown: Optional[int] = None, date_obj: MDate = None,
                            lang: str = 'zh-Hans') -> FestivalCountdownIterable:
    """Return countdown of festivals.
    """
    factory = FestivalFactory(lang=lang)
    return factory.iter_festival_countdown(countdown, date_obj)
