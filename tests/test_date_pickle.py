import unittest
import pickle
from io import BytesIO

from borax.calendars.lunardate import LunarDate
from borax.calendars.festivals2 import WrappedDate


class DatePickleTestCase(unittest.TestCase):

    def test_wd(self):
        ld1 = LunarDate.today()
        fp = BytesIO()

        pickle.dump(ld1, fp)

        fp.seek(0)
        e_ld = pickle.load(fp)
        self.assertEqual(ld1, e_ld)

        wd1 = WrappedDate(ld1)
        fp2 = BytesIO()

        pickle.dump(wd1, fp2)

        fp2.seek(0)
        wd2 = pickle.load(fp2)
        self.assertEqual(wd2, wd1)
