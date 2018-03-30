# coding=utf8

from unittest import TestCase

from borax.structures import AliasDictionary

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


class AliasDictionaryTestCase(TestCase):
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
