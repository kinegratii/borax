import unittest

from borax.calendars.data_parser import strptime
from borax.calendars.lunardate import LunarDate


class ParserTestCase(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(LunarDate(2022, 4, 1), strptime('2022041', '%y%l%m%d'))
        self.assertEqual(LunarDate(2022, 4, 1), strptime('二〇二二041', '%Y%l%m%d'))
        self.assertEqual(LunarDate(2020, 4, 23, 1), strptime('20201423', '%y%l%m%d'))
        self.assertEqual(LunarDate(2022, 4, 23, 0), strptime('二〇二二年四月廿三', '%Y年%M月%D'))
        self.assertEqual(LunarDate(2022, 4, 23, 0), strptime('二〇二二年四月廿三', '%Y年%L%M月%D'))
        self.assertEqual(LunarDate(2020, 4, 23, 1), strptime('二〇二〇年闰四月廿三', '%Y年%L%M月%D'))

    def test_parse_with_cn(self):
        self.assertEqual(LunarDate(2020, 4, 23, 0), strptime('二〇二〇年四月廿三', '%C'))
        self.assertEqual(LunarDate(2020, 4, 23, 1), strptime('二〇二〇年闰四月廿三', '%C'))

        self.assertEqual(LunarDate(2020, 4, 23, 1), LunarDate.strptime('二〇二〇年闰四月廿三', '%C'))
