import unittest

from borax.structures.dictionary import AttributeDict


class AttributeDictTestCase(unittest.TestCase):
    def test_access(self):
        m = AttributeDict({'foo': 'bar'})
        self.assertEqual('bar', m.foo)
        m.foo = 'not bar'
        self.assertEqual('not bar', m['foo'])
