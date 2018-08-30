# coding=utf8

import unittest
import json

from borax.serialize.bjson import BJSONEncoder, EncoderMixin


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __json__(self):
        return [self.x, self.y]


class DPoint(EncoderMixin):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __json__(self):
        return [self.x, self.y, self.z]


class BJsonTestCase(unittest.TestCase):
    def test_json_protocol(self):
        obj = {'point': Point(1, 2)}
        output = json.dumps(obj, cls=BJSONEncoder)
        self.assertEqual('{"point": [1, 2]}', output)

        obj = {'point': DPoint(1, 2, 3)}
        output = json.dumps(obj, cls=BJSONEncoder)
        self.assertEqual('{"point": [1, 2, 3]}', output)
