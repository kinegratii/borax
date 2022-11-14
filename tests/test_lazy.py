import unittest

from borax.patterns.lazy import LazyObject


class MockPoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def create_point():
    return MockPoint(1, 2)


def create_point_with_kwargs(x, y):
    return MockPoint(x, y)


class LazyObjectTestCase(unittest.TestCase):
    def test_lazy_object(self):
        p = LazyObject(create_point)
        self.assertTrue(isinstance(p, LazyObject))
        p.x = 3
        self.assertTrue(isinstance(p, MockPoint))
        self.assertEqual(2, p.y)

    def test_with_kwargs(self):
        p = LazyObject(MockPoint, kwargs={'x': 1, 'y': 2})
        self.assertTrue(isinstance(p, LazyObject))
        self.assertEqual(1, p.x)
        self.assertTrue(isinstance(p, MockPoint))

    def test_delete_attr(self):
        p = LazyObject(MockPoint, kwargs={'x': 1, 'y': 2})
        delattr(p, 'x')
        with self.assertRaises(AttributeError):
            print(p.x)
