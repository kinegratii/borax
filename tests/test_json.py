# coding=utf8

import unittest
import json

from borax.serialize import bjson


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __json__(self):
        return [self.x, self.y]


class DPoint(bjson.EncoderMixin):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __json__(self):
        return [self.x, self.y, self.z]


class BJsonTestCase(unittest.TestCase):
    def test_dumps(self):
        obj = {'point': Point(1, 2), 'a': 4}
        output = bjson.dumps(obj)
        self.assertEqual('{"point": [1, 2], "a": 4}', output)

    def test_custom_encoder(self):
        obj = {'point': Point(1, 2)}
        output = json.dumps(obj, cls=bjson.BJSONEncoder)
        self.assertEqual('{"point": [1, 2]}', output)

        obj = {'point': DPoint(1, 2, 3)}
        output = json.dumps(obj, cls=bjson.BJSONEncoder)
        self.assertEqual('{"point": [1, 2, 3]}', output)
