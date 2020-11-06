# coding=utf8

import copy
import unittest

from borax.datasets.join_ import old_join_one, old_join

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


class JoinOneTestCase(unittest.TestCase):
    def test_with_dict(self):
        catalog_books = old_join_one(books, catalogs_dict, from_='catalog', as_='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])

    def test_with_choices(self):
        catalog_books = old_join_one(books, catalog_choices, from_='catalog', as_='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])

    def test_join_one_with_default(self):
        cur_catalogs_dict = {
            1: 'Python',
            2: 'Java'
        }

        catalog_books = old_join_one(books, cur_catalogs_dict, from_='catalog', as_='catalog_name')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual(None, catalog_books[2]['catalog_name'])

    def test_join_one_with_custom_default(self):
        cur_catalogs_dict = {
            1: 'Python',
            2: 'Java'
        }

        catalog_books = old_join_one(books, cur_catalogs_dict, from_='catalog', as_='catalog_name',
                                     default='[未知分类]')
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('[未知分类]', catalog_books[2]['catalog_name'])


class JoinTestCase(unittest.TestCase):
    def test_as_kwargs(self):
        catalog_books = old_join(books, catalogs_list, from_='catalog', to_='id',
                                 as_kwargs={'name': 'catalog_name'})
        self.assertTrue(all(['catalog_name' in book for book in catalog_books]))
        self.assertEqual('Java', catalog_books[1]['catalog_name'])
        self.assertFalse('catalog_name' in books[1])
