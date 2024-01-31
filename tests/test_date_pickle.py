import unittest
import pickle
from io import BytesIO

from datetime import date

from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals2 import WrappedDate


class WrappedDateBasicTestCase(unittest.TestCase):
    def test_wrapped_date(self):
        ld = LunarDate.today()
        wd = WrappedDate(ld)
        self.assertEqual(ld, wd.lunar)
        with self.assertRaises(AttributeError):
            wd.lunar = LunarDate(2024, 1, 1)


class DatePickleTestCase(unittest.TestCase):

    def test_lunardate_pickle(self):
        ld1 = LunarDate.today()
        fp = BytesIO()

        pickle.dump(ld1, fp)

        fp.seek(0)
        e_ld = pickle.load(fp)
        self.assertEqual(ld1, e_ld)

    def test_wrapped_date_pickle(self):
        wd_list = [WrappedDate(date.today()), WrappedDate(LunarDate.today())]
        for wd in wd_list:
            with self.subTest(wd=wd):
                fp = BytesIO()
                pickle.dump(wd, fp)
                fp.seek(0)
                new_wd = pickle.load(fp)
                self.assertEqual(wd.solar, new_wd.solar)
                self.assertEqual(wd.lunar, new_wd.lunar)
