# coding=utf8
from datetime import date
import unittest

from borax.calendars.lunardate import LunarDate
from borax.calendars.birthday import nominal_age, actual_age_solar, actual_age_lunar


class NominalAgeTestCase(unittest.TestCase):
    def test_nominal_age(self):
        birthday = LunarDate(2017, 6, 16, 1)
        self.assertEqual(1, nominal_age(birthday, LunarDate(2017, 6, 21, 1)))
        self.assertEqual(1, nominal_age(birthday, LunarDate(2017, 12, 29)))
        self.assertEqual(2, nominal_age(birthday, LunarDate(2018, 1, 1)))


class ActualAgeTestCase(unittest.TestCase):
    def test_nominal_age(self):
        self.assertEqual(13, actual_age_solar(date(2004, 3, 1), date(2017, 3, 1)))
        self.assertEqual(12, actual_age_solar(date(2004, 3, 1), date(2017, 2, 28)))

        self.assertEqual(2, actual_age_solar(date(2000, 2, 29), date(2003, 2, 28)))
        self.assertEqual(3, actual_age_solar(date(2000, 2, 29), date(2003, 3, 1)))

        self.assertEqual(3, actual_age_solar(date(2000, 2, 29), date(2004, 2, 28)))
        self.assertEqual(4, actual_age_solar(date(2000, 2, 29), date(2004, 2, 29)))
        self.assertEqual(4, actual_age_solar(date(2000, 2, 29), date(2004, 3, 1)))


class MixedAgeTestCase(unittest.TestCase):
    def test_mixed(self):
        birthday = date(1983, 5, 20)
        self.assertEqual(23, actual_age_solar(birthday, today=date(2007, 5, 19)))
        self.assertEqual(24, actual_age_solar(birthday, today=date(2007, 5, 20)))
        self.assertEqual(24, actual_age_solar(birthday, today=date(2007, 5, 21)))

        #
        self.assertEqual(23, actual_age_lunar(birthday, today=date(2007, 5, 23)))
        self.assertEqual(24, actual_age_lunar(birthday, today=date(2007, 5, 24)))
        self.assertEqual(24, actual_age_lunar(birthday, today=date(2007, 5, 25)))

        self.assertEqual(25, nominal_age(birthday, today=date(2007, 5, 23)))
        self.assertEqual(25, nominal_age(birthday, today=date(2007, 5, 24)))
        self.assertEqual(25, nominal_age(birthday, today=date(2007, 5, 25)))
