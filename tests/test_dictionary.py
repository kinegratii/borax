# coding=utf8

import unittest

from borax.structures.dic import AttributeDict, AliasDict


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


class AliasDictTestCase(unittest.TestCase):
    def test_base(self):
        ad = AliasDict(
            {'biz': True, 'baz': False},
            aliases={'foo': ['bar', 'biz', 'baz']}
        )
        self.assertEqual(False, ad['baz'])

        ad['foo'] = True
        self.assertEqual(True, ad['baz'])
