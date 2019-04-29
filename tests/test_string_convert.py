# coding=utf8

import unittest

from borax.utils import camel2snake, snake2camel

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
