import unittest

from borax.structures.percentage import Percentage


class PercentTestCase(unittest.TestCase):
    def test_basic_use(self):
        p = Percentage(total=100)
        p.increase(34)

        self.assertEqual(100, p.total)
        self.assertEqual(34, p.completed)
        self.assertAlmostEqual(0.34, p.percent)
        self.assertEqual('34.00%', p.percent_display)
        self.assertEqual('34 / 100', p.display)
        self.assertDictEqual({
            'total': 100,
            'completed': 34,
            'percent': 0.34,
            'percent_display': '34.00%',
            'display': '34 / 100'
        }, p.as_dict())

    def test_zero_total(self):
        p = Percentage(total=0)
        p.increase(34)

        self.assertEqual(0, p.total)
        self.assertEqual(34, p.completed)
        self.assertAlmostEqual(0, p.percent)
        self.assertEqual('0.00%', p.percent_display)
        self.assertEqual('34 / 0', p.display)
        self.assertDictEqual({
            'total': 0,
            'completed': 34,
            'percent': 0,
            'percent_display': '0.00%',
            'display': '34 / 0'
        }, p.as_dict())

    def test_custom_places(self):
        p = Percentage(total=100, places=4)
        p.increase(34)

        self.assertEqual(100, p.total)
        self.assertEqual(34, p.completed)
        self.assertAlmostEqual(0.3400, p.percent)
        self.assertEqual('34.0000%', p.percent_display)
        self.assertEqual('34 / 100', p.display)
        self.assertDictEqual({
            'total': 100,
            'completed': 34,
            'percent': 0.3400,
            'percent_display': '34.0000%',
            'display': '34 / 100'
        }, p.as_dict())
