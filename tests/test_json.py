# coding=utf8

import unittest
import json

from borax.serialize import cjson


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __json__(self):
        return [self.x, self.y]


class EPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y


@cjson.to_serializable.register(EPoint)
def encode_epoint(o):
    return [o.x, o.y]


class CJsonTestCase(unittest.TestCase):
    def test_dumps(self):
        obj = {'point': Point(1, 2), 'a': 4}
        output = cjson.dumps(obj)
        expected = ['{"point": [1, 2], "a": 4}', '{"a": 4, "point": [1, 2]}']
        self.assertIn(output, expected)

    def test_custom_encoder(self):
        obj = {'point': Point(1, 2)}
        output = json.dumps(obj, default=cjson.encoder)
        self.assertEqual('{"point": [1, 2]}', output)

    def test_singledispatch(self):
        obj = {'point': EPoint(1, 2)}
        output = cjson.dumps(obj)
        self.assertEqual('{"point": [1, 2]}', output)

    def test_mixed_encoder(self):
        class Pt:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __json__(self):
                return [self.x, self.y]

        @cjson.to_serializable.register(Pt)
        def encode_pt(p):
            return {'x': p.x, 'y': p.y}

        obj = {'point': Pt(1, 2)}
        output = cjson.dumps(obj)
        self.assertEqual('{"point": {"x": 1, "y": 2}}', output)

        cjson.encoder.register(Pt, cjson.encode_object)

        obj = {'point': Pt(1, 2)}
        output = cjson.dumps(obj)
        self.assertEqual('{"point": [1, 2]}', output)
