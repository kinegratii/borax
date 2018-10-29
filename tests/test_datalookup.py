# coding=utf8

import unittest

from borax.structures.lookup import TableLookup


class TableLookupTestCase(unittest.TestCase):
    def test_base(self):
        dataset = TableLookup(['a', 'b', 'c', 'd']).feed([
            [1, 2, 3, 4],
            [11, 12, 13, 14],
            [21, 22, 23, 24]
        ])

        c = dataset.find(1)
        self.assertEqual(1, c.a)
        self.assertEqual(2, c.b)
        self.assertEqual(3, c.c)
