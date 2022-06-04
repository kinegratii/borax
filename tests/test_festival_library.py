import unittest
from datetime import date
from io import StringIO
from unittest.mock import MagicMock, patch

from borax.calendars.festivals2 import LunarFestival, TermFestival, FestivalLibrary


class FestivalLibraryTestCase(unittest.TestCase):
    def test_library(self):
        fl = FestivalLibrary.load_builtin()
        self.assertEqual(33, len(fl))

        spring_festival = fl.get_festival('春节')
        self.assertTrue(isinstance(spring_festival, LunarFestival))

        names = fl.get_festival_names(date_obj=date(2021, 10, 1))
        self.assertListEqual(['国庆节'], names)

        gd_days = []
        for nday, gd_list in fl.iter_festival_countdown(date_obj=date(2021, 1, 1), countdown=31):
            gd_days.extend(gd_list)

        self.assertIn('元旦', [g.name for g in gd_days])

    def test_list_days(self):
        fl = FestivalLibrary.load_builtin()
        fes_list = []
        for _, wd, festival in fl.list_days_in_countdown(countdown=365):
            fes_list.append(festival.name)
        self.assertIn('元旦', fes_list)

        festival_names = [items[1].name for items in fl.list_days(date(2022, 1, 1), date(2022, 12, 31))]
        self.assertIn('元旦', festival_names)


class FestivalLibraryUniqueTestCase(unittest.TestCase):
    def test_unique(self):
        fl = FestivalLibrary()
        ft1 = TermFestival(name='冬至')
        fl.append(ft1)
        self.assertEqual(1, len(fl.get_code_set()))
        ft2 = TermFestival(index=23)
        fl.extend_unique([ft2])
        self.assertEqual(1, len(fl))
        ft3 = TermFestival(name='小寒')
        fl.extend_unique([ft3])
        self.assertEqual(2, len(fl))
        fl.extend_unique(['205026', '89005'])
        self.assertEqual(3, len(fl))

    def test_edit(self):
        fl = FestivalLibrary()
        fl.load_term_festivals()
        self.assertEqual(24, len(fl))

    def test_save(self):
        fileobj = StringIO()
        fl = FestivalLibrary.load_builtin()
        fl.to_csv(fileobj)

        mock = MagicMock()
        mock.write.return_value = None
        with patch('builtins.open', mock):
            fl.to_csv('xxx.csv')

    def test_filter(self):
        fl = FestivalLibrary.load_builtin('ext1')
        basic_fl = fl.filter(catalogs='basic')
        self.assertTrue(len(basic_fl) > 0)


class FestivalLibraryCalendarTestCase(unittest.TestCase):
    def test_calendar(self):
        fl = FestivalLibrary.load_builtin()
        days = fl.monthdaycalendar(2022, 1)
        self.assertEqual(6, len(days))
