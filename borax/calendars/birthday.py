from dataclasses import dataclass
from datetime import date, timedelta
from typing import Union

from .festivals2 import WrappedDate, LunarFestival, SolarFestival
from .lunardate import LunarDate, LCalendars


def nominal_age(birthday, today=None):
    birthday = LCalendars.cast_date(birthday, LunarDate)
    if today:
        today = LCalendars.cast_date(today, LunarDate)
    else:
        today = LunarDate.today()
    return today.year - birthday.year + 1


def actual_age_solar(birthday, today=None):
    """See more at https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python/9754466#9754466
    :param birthday:
    :param today:
    :return:
    """
    birthday = LCalendars.cast_date(birthday, date)
    if today:
        today = LCalendars.cast_date(today, date)
    else:
        today = date.today()
    return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))


def actual_age_lunar(birthday, today=None):
    birthday = LCalendars.cast_date(birthday, LunarDate)
    if today:
        today = LCalendars.cast_date(today, LunarDate)
    else:
        today = LunarDate.today()
    return today.year - birthday.year - (
            (today.month, today.leap, today.day) < (birthday.month, birthday.leap, birthday.day)
    )


@dataclass
class BirthdayResult:
    nominal_age: int = 0  # 虚岁
    actual_age: int = 0  # 周岁
    animal: str = ''
    birthday_str: str = ''
    next_solar_birthday: WrappedDate = None
    next_lunar_birthday: WrappedDate = None
    living_day_count: int = 0


class BirthdayCalculator:
    def __init__(self, birthday: Union[date, LunarDate]):
        self._birthday: WrappedDate = WrappedDate(birthday)
        self._sbf = SolarFestival(freq='y', month=self._birthday.solar.month, day=self._birthday.solar.day)
        self._lbf = LunarFestival(freq='y', month=self._birthday.lunar.month, day=self._birthday.lunar.day,
                                  leap=self._birthday.lunar.leap)

    @property
    def birthday(self) -> WrappedDate:
        return self._birthday

    @property
    def solar_birthday_festival(self) -> SolarFestival:
        return self._sbf

    @property
    def lunar_birthday_festival(self) -> LunarFestival:
        return self._lbf

    def calculate(self, this_day=None) -> BirthdayResult:
        """Calculate one's age and birthday info based on a given date."""
        if this_day is None:
            this_date = WrappedDate(date.today())
        else:
            this_date = WrappedDate(this_day)
        result = BirthdayResult(animal=self._birthday.lunar.animal, birthday_str=self._birthday.full_str())
        result.nominal_age = nominal_age(self._birthday, this_date.lunar)
        result.actual_age = actual_age_solar(self._birthday, this_date.solar)
        result.next_lunar_birthday = self._lbf.list_days(start_date=this_date, count=1)[0]
        result.next_solar_birthday = self._sbf.list_days(start_date=this_date, count=1)[0]
        result.living_day_count = (this_date - self._birthday).days
        return result

    def list_days_in_same_day(self, start_date=None, end_date=None) -> list[WrappedDate]:
        """Return the days in a same days by solar and lunar birthday"""
        if start_date is None:
            start_date = self.birthday + timedelta(days=1)
        wrapped_date_list = []
        for wd in self._sbf.list_days(start_date, end_date):
            if wd.lunar.month == self.birthday.lunar.month and wd.lunar.day == self.birthday.lunar.day:
                wrapped_date_list.append(wd)
        return wrapped_date_list
