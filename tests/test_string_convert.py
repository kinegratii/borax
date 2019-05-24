# coding=utf8

import unittest

from borax.strings import camel2snake, snake2camel, get_percentage_display

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
