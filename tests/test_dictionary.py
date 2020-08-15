# coding=utf8

import unittest

from borax.structures.dictionary import AliasDictionary, AttributeDict


class AttributeDictTestCase(unittest.TestCase):
    def test_access(self):
        m = AttributeDict({'foo': 'bar'})
        self.assertEqual('bar', m.foo)
        m.foo = 'not bar'
        self.assertEqual('not bar', m['foo'])

    def test_first(self):
        m = AttributeDict({'foo': 'bar', 'biz': 'baz'})
        value = m.first('wrong', 'incorrect', 'foo', 'biz')
        self.assertEqual('bar', value)


demo_data = {
    'alias': {
        'A': 'a',
        'A1': 'a',
        'B': 'b',
        'D': 'd',
        'P': 'e'
    },
    'data': {
        'a': 'apple',
        'b': 'banana',
        'e': 'egg',
        'o': 'orange',
        'P': 'pear'

    }
}


class AliasDictionaryTestCase(unittest.TestCase):
    def test_test(self):
        ad = AliasDictionary(demo_data['data'], demo_data['alias'])
        self.assertEqual('apple', ad.get('a'))
        self.assertEqual('CC', ad.get('c', 'CC'))

    def test_get_item(self):
        ad = AliasDictionary(demo_data['data'], demo_data['alias'])
        self.assertTupleEqual(
            ('a', 'a', 'apple'),
            ad.get_item('a')
        )
        self.assertTupleEqual(
            ('A', 'a', 'apple'),
            ad.get_item('A')
        )
        self.assertTupleEqual(
            ('P', 'P', 'pear'),
            ad.get_item('P')
        )

        with self.assertRaises(KeyError):
            ad.get_item('D')
        self.assertTupleEqual(
            ('D', None, 'D'),
            ad.get_item('D', default='D')
        )
        with self.assertRaises(KeyError):
            ad.get_item('E')
        self.assertTupleEqual(
            ('E', None, 'E'),
            ad.get_item('E', default='E')
        )

    def test_get_available_items(self):
        ad = AliasDictionary(demo_data['data'], demo_data['alias'])
        for key, value, aliases in ad.get_available_items():
            if key == 'a':
                self.assertSetEqual({'A', 'A1'}, set(aliases))
