import unittest

from borax.structures.tree import pll2cnl, _parse_extra_data


class TreeFetcherTestCase(unittest.TestCase):
    def test_parse_extra(self):
        source = {'id': 0, 'name': 'A', 'parent': None}
        extra_data = _parse_extra_data(
            source,
            flat_fields=[],
            extra_fields=[],
            extra_key=None,
            trs_fields=['id', 'parent']
        )
        self.assertDictEqual({'name': 'A'}, extra_data)
        extra_data = _parse_extra_data(
            source,
            flat_fields=[],
            extra_fields=['name'],
            extra_key="extra",
            trs_fields=['id', 'parent']
        )

        self.assertDictEqual({'extra': {'name': 'A'}}, extra_data)

    def test_pll2cnl(self):
        source = [
            {'id': 0, 'name': 'A', 'parent': None},
            {'id': 1, 'name': 'B', 'parent': 0},
            {'id': 2, 'name': 'C', 'parent': 0},
            {'id': 3, 'name': 'D', 'parent': 0},
            {'id': 4, 'name': 'E', 'parent': 1},
            {'id': 5, 'name': 'F', 'parent': 1},
            {'id': 6, 'name': 'H', 'parent': 3},
            {'id': 7, 'name': 'I', 'parent': 3},
            {'id': 8, 'name': 'J', 'parent': 3},
        ]

        children_list = pll2cnl(source)
        self.assertEqual(0, children_list[0]['id'])
        self.assertEqual('B', children_list[0]['children'][0]['name'])

        children_list1 = pll2cnl(source, flat_fields=['name'])
        self.assertEqual(0, children_list1[0]['id'])
        self.assertEqual('B', children_list1[0]['children'][0]['name'])

        self.assertSequenceEqual(children_list, children_list1)

        with self.assertRaises(ValueError):
            pll2cnl(source, extra_key='parent')
        with self.assertRaises(ValueError):
            pll2cnl(source, flat_fields=['parent'])
        with self.assertRaises(ValueError):
            pll2cnl(source, flat_fields=['foo'])

    def test_forward_reference(self):
        source = [
            {'id': 0, 'name': 'A', 'parent': None},
            {'id': 1, 'name': 'B', 'parent': 3},
            {'id': 2, 'name': 'C', 'parent': 0},
            {'id': 3, 'name': 'D', 'parent': 0},
        ]
        data = pll2cnl(source)
        self.assertIsNotNone(data)
