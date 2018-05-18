# coding=utf8

import unittest

from borax.utils import force_iterable


class IterableTestCase(unittest.TestCase):
    def test_force_iterable(self):
        self.assertListEqual([1], force_iterable(1))
        self.assertListEqual([1, 2], force_iterable([1, 2]))
