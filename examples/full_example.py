# coding=utf8
"""The full example for calendars package.
"""
from borax.calendars.lunardate import LunarDate, LCalendars
from borax.calendars.birthday import actual_age_lunar, actual_age_solar, nominal_age

ld = LunarDate(2001, 11, 6)
print(ld.to_solar_date())
print(LCalendars.delta(LunarDate.today(), ld))
print(ld.encode())
print(nominal_age(ld))
print(actual_age_solar(ld))
print(actual_age_lunar(ld))
