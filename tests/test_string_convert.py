# coding=utf8

from datetime import datetime

import unittest
from unittest.mock import Mock, patch

from borax.strings import camel2snake, snake2camel, get_percentage_display
from borax.system import rotate_filename, SUFFIX_DT_UNDERLINE

FIXTURES = [
    ('HelloWord', 'hello_word'),
    ('A', 'a'),
    ('Aa', 'aa'),
    ('Act', 'act'),
    ('AcTa', 'ac_ta')
]


class StringConvertTestCase(unittest.TestCase):
    def test_all(self):
        for cs, ss in FIXTURES:
            with self.subTest(cs=cs, ss=ss):
                self.assertEqual(cs, snake2camel(ss))
                self.assertEqual(ss, camel2snake(cs))


class PercentageStringTestCase(unittest.TestCase):
    def test_convert(self):
        self.assertEqual('100.00%', get_percentage_display(1, places=2))
        self.assertEqual('56.23%', get_percentage_display(0.5623))


class FilenameRotateTestCase(unittest.TestCase):
    @patch('borax.system.datetime')
    def test_rotate(self, my_datetime):
        my_datetime.now = Mock(return_value=datetime(2019, 5, 25))
        self.assertEqual(
            'demo_20190525.docx',
            rotate_filename('demo.docx', time_fmt='%Y%m%d')
        )
        self.assertEqual(
            'demo-2019_05_25.docx',
            rotate_filename('demo.docx', time_fmt='%Y_%m_%d', sep='-')
        )

        self.assertEqual(
            'demo-2019_05_25.docx',
            rotate_filename('demo.docx', time_fmt='%Y_%m_%d', sep='-')
        )
        # Full path
        self.assertEqual(
            '/usr/home/pi/demo-2019_05_25.docx',
            rotate_filename('/usr/home/pi/demo.docx', time_fmt='%Y_%m_%d', sep='-')
        )
        # name with a dot char.
        self.assertEqual(
            '/usr/home/pi/bws-v3.2.1-upgrade_2019_05_25.sql',
            rotate_filename('/usr/home/pi/bws-v3.2.1-upgrade.sql', time_fmt='%Y_%m_%d', sep='_')
        )

    def test_with_one_datetime(self):
        now = datetime(2019, 5, 23, 10, 22, 23)
        self.assertEqual(
            'demo_20190523102223.docx',
            rotate_filename('demo.docx', now=now)
        )
        self.assertEqual(
            'demo-2019_05_23_10_22_23.docx',
            rotate_filename('demo.docx', time_fmt=SUFFIX_DT_UNDERLINE, sep='-', now=now)
        )

        self.assertEqual(
            'demo-2019_05_23.docx',
            rotate_filename('demo.docx', time_fmt='%Y_%m_%d', sep='-', now=now)
        )
        # Full path
        self.assertEqual(
            '/usr/home/pi/demo-2019_05_23.docx',
            rotate_filename('/usr/home/pi/demo.docx', time_fmt='%Y_%m_%d', sep='-', now=now)
        )
        # name with a dot char.
        self.assertEqual(
            '/usr/home/pi/bws-v3.2.1-upgrade_2019_05_23.sql',
            rotate_filename('/usr/home/pi/bws-v3.2.1-upgrade.sql', time_fmt='%Y_%m_%d', sep='_', now=now)
        )
