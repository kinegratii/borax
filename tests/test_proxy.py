import unittest

from borax.patterns.proxy import Proxy


class MockPoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_distance(self):
        return self.x ** 2 + self.y ** 2


class ProxyTestCase(unittest.TestCase):
    def test_proxy(self):
        proxy = Proxy()
        with self.assertRaises(AttributeError):
            proxy.get_distance()
        proxy.initialize(MockPoint(3, 4))
        self.assertEqual(25, proxy.get_distance())
