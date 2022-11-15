from datetime import date

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
