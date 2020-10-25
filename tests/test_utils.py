# coding=utf8

import itertools
import unittest
from unittest.mock import Mock

from borax.utils import force_iterable, trim_iterable, firstof, get_item_cycle, chain_getattr, force_list


class BaseTestCase(unittest.TestCase):
    def test_force_iterable(self):
        self.assertListEqual([1], force_iterable(1))
        self.assertListEqual([1, 2], force_iterable([1, 2]))

    def test_item_cycle(self):
        data = list(range(0, 10))
        self.assertEqual(6, get_item_cycle(data, 6))

    def test_item_cycle2(self):
        source = list(range(7))
        total = 1232
        for index, ele in enumerate(itertools.cycle(source)):
            if index > total:
                break
            self.assertEqual(ele, get_item_cycle(source, index))

    def test_chain(self):
        c = Mock(a=Mock(c='ac'))
        self.assertEqual('ac', chain_getattr(c, 'a.c'))
        d = object()
        self.assertEqual('default', chain_getattr(d, 'b.c', 'default'))


class StringTrimTestCase(unittest.TestCase):
    def test_trim_list(self):
        # note: [4, 5, 6, 5, 1, 1,5]
        elements = ['1212', '34343', '783454', '23904', '2', '1', '30992']

        expect = trim_iterable(elements, 10)
        self.assertListEqual(['1212', '34343'], expect)
        expect = trim_iterable(elements, 9)
        self.assertListEqual(['1212', '34343'], expect)
        expect = trim_iterable(elements, 3)
        self.assertListEqual([], expect)

        result = trim_iterable(elements, 20, split='/')
        self.assertEqual('1212/34343/783454', result)
        result = trim_iterable(elements, 9, split='/')
        self.assertEqual('1212', result)

        result = trim_iterable(elements, 18, split='', prefix='X')
        self.assertEqual('X1212X34343X783454', result)

        result = trim_iterable(elements, 18, split='-', prefix='X')
        self.assertEqual('X1212-X34343', result)


class FirstofTestCase(unittest.TestCase):
    def test_first_of(self):
        self.assertEqual(3, firstof([None, None, 3, 4]))
        self.assertEqual(3, firstof([None, None, None, None], default=3))


class ForceListTestCase(unittest.TestCase):
    def test_force_list(self):
        self.assertTupleEqual((1, 2), force_list((1, 2)))
        self.assertTupleEqual(('1', '2'), force_list('1,2'))
        self.assertTupleEqual((1,), force_list(1))
