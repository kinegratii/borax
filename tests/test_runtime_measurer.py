import unittest

from borax.devtools import RuntimeMeasurer


def long_operate():
    for _ in range(100000):
        pass


class RuntimeMeasurerTestCase(unittest.TestCase):
    def test_one_hit(self):
        rm = RuntimeMeasurer()
        rm.start('xt')
        long_operate()
        rm.end('xt')
        data = rm.get_measure_result()
        self.assertEqual(1, data['xt'].count)
        self.assertIsNotNone(data['xt'].avg)

    def test_with(self):
        rm = RuntimeMeasurer()
        with rm.measure('xt'):
            long_operate()
        data = rm.get_measure_result()
        self.assertEqual(1, data['xt'].count)
        self.assertIsNotNone(data['xt'].avg)

    def test_multiple_tags(self):
        rm = RuntimeMeasurer()
        rm.start('tag1')
        long_operate()
        rm.end('tag1').start('tag2')
        long_operate()
        rm.end('tag2')
        data = rm.get_measure_result()
        self.assertTrue('tag1' in data)
        self.assertTrue('tag2' in data)
