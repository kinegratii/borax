# coding=utf8
import datetime

__all__ = ['LunarDate']

_START_SOLAR_DATE = datetime.date(1900, 1, 31)
_END_SOLAR_DATE = datetime.date(2101, 1, 8)
_MAX_OFFSET = (_END_SOLAR_DATE - _START_SOLAR_DATE).days  # 73391
_START_LUNAR_YEAR = 1900
_END_LUNAR_YEAR = 2100

YEAR_INFOS = [
    #    /* encoding:
    #               b bbbbbbbbbbbb bbbb
    #       bit#    1 111111000000 0000
    #               6 543210987654 3210
    #               . ............ ....
    #       month#    000000000111
    #               M 123456789012   L
    #
    #    b_j = 1 for long month, b_j = 0 for short month
    #    L is the leap month of the year if 1<=L<=12; NO leap month if L = 0.
    #    The leap month (if exists) is long one iff M = 1.
    #    */
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,  # 1900 - 1909
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,  # 1910 - 1919
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,  # 1920 - 1929
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,  # 1930 - 1939
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,  # 1940 - 1949
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,  # 1950 - 1959
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,  # 1960 - 1969
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,  # 1970 - 1979
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,  # 1980 - 1989
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,  # 1990 - 1999
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,  # 2000 - 2009
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,  # 2010 - 2019
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,  # 2020 - 2029
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,  # 2030 - 2039
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,  # 2040 - 2049
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,  # 2050 - 2059
    0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,  # 2060 - 2069
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,  # 2070 - 2079
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,  # 2080 - 2089
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,  # 2090 - 2099
    0x0d520
]


def parse_year_days(year_info):
    """Parse year days from a year info.
    """
    year_info = int(year_info)
    res = 29 * 12

    leap = False
    if year_info % 16 != 0:
        leap = True
        res += 29

    year_info //= 16

    for i in range(12 + leap):
        if year_info % 2 == 1:
            res += 1
        year_info //= 2
    return res


YEAR_DAYS = [parse_year_days(x) for x in YEAR_INFOS]


def iter_year_month(year_info):
    """ Iter the month days in a lunar year.
    """
    # info => month, days, leap
    months = [(i, 0) for i in range(1, 13)]
    leap_month = year_info % 16  # The leap month in this year.
    if leap_month == 0:
        pass
    elif leap_month <= 12:
        months.insert(leap_month, (leap_month, 1))
    else:
        raise ValueError("yearInfo %r mod 16 should in [0, 12]" % year_info)

    for month, leap in months:
        if leap:
            days = (year_info >> 16) % 2 + 29
        else:
            days = (year_info >> (16 - month)) % 2 + 29
        yield month, days, leap


# offset <----> year, day_offset <----> year, month, day, leap

def offset2ymdl(offset):
    def _o2mdl(_year_info, _offset):
        for _month, _days, _leap in iter_year_month(_year_info):
            if _offset < _days:
                break
            _offset -= _days
        else:
            raise ValueError('Out of range.')
        return _month, _offset + 1, _leap

    offset = int(offset)

    for idx, yearDay in enumerate(YEAR_DAYS):
        if offset < yearDay:
            break
        offset -= yearDay
    else:
        raise ValueError('Out of range')
    year = _START_LUNAR_YEAR + idx

    year_info = YEAR_INFOS[idx]
    month, day, leap = _o2mdl(year_info, offset)
    return year, month, day, leap


def ymdl2offset(year, month, day, leap):
    def _mdl2o(_year_info, _month, _day, _leap):
        _leap = int(_leap)
        res = 0
        for _month_, _days_, _leap_ in iter_year_month(_year_info):
            if (_month_, _leap_) == (_month, _leap):
                if 1 <= _day <= _days_:
                    res += _day - 1
                    return res
                else:
                    raise ValueError("day out of range")
            res += _days_

        raise ValueError("month out of range")

    offset = 0
    if year < _START_LUNAR_YEAR or year > _END_LUNAR_YEAR:
        raise ValueError('year out of range [1900, 2100]')
    year_idx = year - _START_LUNAR_YEAR
    for i in range(year_idx):
        offset += YEAR_DAYS[i]

    offset += _mdl2o(YEAR_INFOS[year_idx], month, day, leap)
    return offset


class LunarDate:
    __slots__ = '_year', '_month', '_day', '_leap', '_offset'

    def __new__(cls, year, month, day, leap=False):
        self = object.__new__(cls)
        offset = ymdl2offset(year, month, day, leap)
        self._year = year
        self._month = month
        self._day = day
        self._leap = leap
        self._offset = offset
        return self
        # TODO Add validate or raise ValueError

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @property
    def leap(self):
        return self._leap

    def __str__(self):
        return 'LunarDate(%d, %d, %d, %d)' % (self.year, self.month, self.day, self.leap)

    __repr__ = __str__

    @staticmethod
    def from_solar_date(year, month, day):
        solar_date = datetime.date(year, month, day)
        offset = (solar_date - _START_SOLAR_DATE).days
        y, m, d, l = offset2ymdl(offset)
        return LunarDate(y, m, d, l)

    def to_solar_date(self):
        offset = ymdl2offset(self.year, self.month, self.day, self.leap)
        return _START_SOLAR_DATE + datetime.timedelta(days=offset)

    def __sub__(self, other):
        if isinstance(other, LunarDate):
            return self.to_solar_date() - other.to_solar_date()
        elif isinstance(other, datetime.date):
            return self.to_solar_date() - other
        elif isinstance(other, datetime.timedelta):
            res = self.to_solar_date() - other
            return LunarDate.from_solar_date(res.year, res.month, res.day)
        raise TypeError

    def __rsub__(self, other):
        if isinstance(other, datetime.date):
            return other - self.to_solar_date()

    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            res = self.to_solar_date() + other
            return LunarDate.from_solar_date(res.year, res.month, res.day)
        raise TypeError

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        if not isinstance(other, LunarDate):
            return False

        return self - other == datetime.timedelta(0)

    def __lt__(self, other):
        try:
            return self - other < datetime.timedelta(0)
        except TypeError:
            raise TypeError("can't compare LunarDate to %s" % (type(other).__name__,))

    def __le__(self, other):
        # needed because the default implementation tries equality first,
        # and that does not throw a type error
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __hash__(self):
        return hash((self.year, self.month, self.day, self.leap))

    @classmethod
    def today(cls):
        res = datetime.date.today()
        return cls.from_solar_date(res.year, res.month, res.day)


LunarDate.min = LunarDate(1990, 1, 1, 0)
LunarDate.max = LunarDate(2100, 12, 29, 0)
