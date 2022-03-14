# coding=utf8


import unittest

from borax.datasets.fetch import fetch, fetch_single, ifetch_multiple, fetch_as_dict, bget

DICT_LIST_DATA = [
    {'id': 282, 'name': 'Alice', 'age': 30, 'sex': 'female'},
    {'id': 217, 'name': 'Bob', 'age': 56},
    {'id': 328, 'name': 'Charlie', 'age': 56, 'sex': 'male'},
]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GetterTestCase(unittest.TestCase):
    def test_default_getter(self):
        p = Point(1, 2)
        self.assertEqual(1, bget(p, 'x'))
        p2 = [2, 4]
        self.assertEqual(4, bget(p2, 1))
        p3 = {'x': 5, 'y': 10}
        self.assertEqual(5, bget(p3, 'x'))


class FetchTestCase(unittest.TestCase):
    def test_fetch_single(self):
        names = fetch_single(DICT_LIST_DATA, 'name')
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        sexs = fetch_single(DICT_LIST_DATA, 'sex', default='male')
        self.assertListEqual(sexs, ['female', 'male', 'male'])

    def test_ifetch_multiple(self):
        names, ages = map(list, ifetch_multiple(DICT_LIST_DATA, 'name', 'age'))
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])

    def test_fetch(self):
        names = fetch(DICT_LIST_DATA, 'name')
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])

        sexs = fetch(DICT_LIST_DATA, 'sex', default='male')
        self.assertListEqual(sexs, ['female', 'male', 'male'])

        names, ages = fetch(DICT_LIST_DATA, 'name', 'age')
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])

        names, ages, sexs = fetch(DICT_LIST_DATA, 'name', 'age', 'sex', defaults={'sex': 'male'})
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])
        self.assertListEqual(sexs, ['female', 'male', 'male'])


class MockItem:
    def __init__(self, x, y, z):
        self._data = {'x': x, 'y': y, 'z': z}

    def get(self, key):
        return self._data.get(key)


class FetchCustomGetterTestCase(unittest.TestCase):
    def test_custom_getter(self):
        data_list = [MockItem(1, 2, 3), MockItem(4, 5, 6), MockItem(7, 8, 9)]
        xs, ys, zs = fetch(data_list, 'x', 'y', 'z', getter=lambda item, key: item.get(key))
        self.assertListEqual([1, 4, 7], xs)

    def test_with_dict(self):
        """
        Use dict.get(key) to pick item.
        """
        names, ages = fetch(DICT_LIST_DATA, 'name', 'age', getter=lambda item, key: item.get(key))
        self.assertListEqual(names, ['Alice', 'Bob', 'Charlie'])
        self.assertListEqual(ages, [30, 56, 56])


class FetchAsDictTestCase(unittest.TestCase):
    def test_fetch_as_dict(self):
        objects = [
            {'id': 282, 'name': 'Alice', 'age': 30},
            {'id': 217, 'name': 'Bob', 'age': 56},
            {'id': 328, 'name': 'Charlie', 'age': 56},
        ]
        data_dict = fetch_as_dict(objects, 'id', 'name')
        self.assertDictEqual({282: 'Alice', 217: 'Bob', 328: 'Charlie'}, data_dict)


class FetchFromTuplesTestCase(unittest.TestCase):
    def test_fetch_from_tuples(self):
        data = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [11, 12, 13, 14, 15, 16, 17, 18, 19],
            [21, 22, 23, 24, 25, 26, 27, 28, 29]
        ]
        ones, threes = fetch(data, 0, 2)
        self.assertListEqual(ones, [1, 11, 21])
        self.assertListEqual(threes, [3, 13, 23])
