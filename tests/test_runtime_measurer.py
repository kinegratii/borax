# coding=utf8
import time
import unittest

from borax.runtime import RuntimeMeasurer


def long_operate():
    time.sleep(1)


class RuntimeMeasurerTestCase(unittest.TestCase):
    def test_one_hit(self):
        rm = RuntimeMeasurer()
        rm.start('xt')
        long_operate()
        rm.end('xt')
        data = rm.get_measure_data()[0]
        self.assertEqual(1, data['total'])
        self.assertAlmostEqual(1, data['avg'], places=2)

    def test_with(self):
        rm = RuntimeMeasurer()
        with rm.measure('xt'):
            long_operate()
        data = rm.get_measure_data()[0]
        self.assertEqual(1, data['total'])
        self.assertAlmostEqual(1, data['avg'], places=2)
