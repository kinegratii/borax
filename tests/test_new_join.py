# coding=utf8

import unittest
import copy

from borax.datasets.join_ import (OnClause, OC, SelectClause, SC, join, join_one)

catalogs_dict = {
    1: 'Python',
    2: 'Java',
    3: '软件工程'
}
catalog_choices = [(1, 'Python'), (2, 'Java'), (3, '软件工程')]
catalogs_list = [
    {'id': 1, 'name': 'Python'},
    {'id': 2, 'name': 'Java'},
    {'id': 3, 'name': '软件工程'},
]
books = [
    {'name': 'Python入门教程', 'catalog': 1, 'price': 45},
    {'name': 'Java标准库', 'catalog': 2, 'price': 80},
    {'name': '软件工程(本科教学版)', 'catalog': 3, 'price': 45},
    {'name': 'Django Book', 'catalog': 1, 'price': 45},
    {'name': '系统架构设计教程', 'catalog': 3, 'price': 104},
]


class OnClauseTestCase(unittest.TestCase):
    def test_type_hints(self):
        c1 = OnClause("foo", "foo")
        self.assertEqual("OnClause", c1.__class__.__name__)
        self.assertTrue(isinstance(c1, tuple))
        alias_obj = OC("foo")
        self.assertEqual("OnClause", alias_obj.__class__.__name__)
        self.assertTrue(isinstance(alias_obj, tuple))

    def test_build(self):
        expected = ("foo", "foo")
        self.assertEqual(expected, OnClause.from_val("foo"))
        self.assertEqual(expected, OnClause.from_val(("foo",)))
        self.assertEqual(expected, OnClause.from_val(("foo", "foo")))
        self.assertEqual(expected, OnClause.from_val(OnClause("foo")))
        with self.assertRaises(TypeError):
            OnClause.from_val(["foo", "bar"])


class SelectClauseTestCase(unittest.TestCase):
    def test_type_hints(self):
        c1 = SelectClause("foo", "foo")
        self.assertEqual("SelectClause", c1.__class__.__name__)
        self.assertTrue(isinstance(c1, tuple))
        alias_obj = SC("foo")
        self.assertEqual("SelectClause", alias_obj.__class__.__name__)
        self.assertTrue(isinstance(alias_obj, tuple))

    def test_build(self):
        expected = ("foo", "foo", None)
        self.assertEqual(expected, SelectClause.from_val("foo"))
        self.assertEqual(expected, SelectClause.from_val(("foo",)))
        self.assertEqual(expected, SelectClause.from_val(("foo", "foo")))
        self.assertEqual(expected, SelectClause.from_val(SelectClause("foo")))
        with self.assertRaises(TypeError):
            OnClause.from_val(["foo", "bar"])


class JoinOneTestCase(unittest.TestCase):
    def test_with_dict(self):
        catalog_books = join_one(books, catalogs_dict, on='catalog', select_as='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])

    def test_with_choices(self):
        catalog_books = join_one(books, catalog_choices, on='catalog', select_as='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])

    def test_join_one_with_default(self):
        cur_catalogs_dict = {
            1: 'Python',
            2: 'Java'
        }

        catalog_books = join_one(books, cur_catalogs_dict, on='catalog', select_as='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual(None, catalog_books[2]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])

    def test_join_one_with_custom_default(self):
        cur_catalogs_dict = {
            1: 'Python',
            2: 'Java'
        }
        catalog_books = join_one(books, cur_catalogs_dict, on='catalog', select_as='catalog_name',
                                 default='[未知分类]')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('[未知分类]', catalog_books[2]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])

    def test_callback(self):
        def _on(_litem):
            return _litem['catalog']

        catalog_books = join_one(books, catalogs_dict, on=_on, select_as='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])


class JoinTestCase(unittest.TestCase):
    def test_basic_join(self):
        catalog_books = join(books, catalogs_list, on=('catalog', 'id'),
                             select_as=('name', 'catalog_name'))
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])
