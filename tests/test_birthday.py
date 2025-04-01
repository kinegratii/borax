import unittest
from datetime import date

from borax.calendars.birthday import nominal_age, actual_age_solar, actual_age_lunar, BirthdayCalculator
from borax.calendars.festivals2 import WrappedDate
from borax.calendars.lunardate import LunarDate


class BirthdayCalculatorTestCase(unittest.TestCase):
    def test_solar_birthday(self):
        bc1 = BirthdayCalculator(date(2000, 3, 4))  # LunarDate(2000, 1, 29)

        result = bc1.calculate(date(2010, 3, 3))
        self.assertEqual(9, result.actual_age)
        self.assertEqual(11, result.nominal_age)

        result1 = bc1.calculate(date(2010, 3, 4))
        self.assertEqual(10, result1.actual_age)
        self.assertEqual(11, result1.nominal_age)

        result2 = bc1.calculate(LunarDate(2009, 12, 30))
        self.assertEqual(10, result2.nominal_age)

        result3 = bc1.calculate(LunarDate(2010, 1, 1))
        self.assertEqual(11, result3.nominal_age)

    def test_leap_feb(self):
        bc = BirthdayCalculator(date(2020, 2, 29))
        result = bc.calculate(date(2021, 2, 28))
        self.assertEqual(0, result.actual_age)
        result = bc.calculate(date(2021, 3, 1))
        self.assertEqual(1, result.actual_age)

    def test_same_days(self):
        my_birthday = LunarDate(2004, 2, 2)
        this_day = date(2023, 1, 1)
        my_bc = BirthdayCalculator(my_birthday)
        same_day_list = my_bc.list_days_in_same_day(start_date=this_day)
        self.assertIn(WrappedDate(LunarDate(2023, 2, 2)), same_day_list)


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
