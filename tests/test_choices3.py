# coding=utf8

import unittest

from borax import choices3


class BItemTestCase(unittest.TestCase):
    def test_choice_item_equal(self):
        c = choices3.BItem(4, 'Demo')
        self.assertTrue(c == 4)
        self.assertTrue(4 == c)
        self.assertFalse(c != 4)
        self.assertFalse(4 != c)
        self.assertEqual(4, c)

    def test_member(self):
        members = [
            choices3.BItem(2, 'A'),
            choices3.BItem(3, 'B'),
            choices3.BItem(4, 'C')
        ]
        self.assertTrue(2 in members)


class Demo1Field(choices3.BChoices):
    A = 1, 'VER'
    B = 2, 'STE'
    c = 3, 'SSS'
    D = 5
    _E = 6, 'ES'
    F = 8
    G = choices3.BItem(10, 'G')


class FieldChoiceTestCase(unittest.TestCase):
    def test_get_value(self):
        self.assertEqual(1, Demo1Field.A)
        self.assertEqual(2, Demo1Field.B)
        self.assertEqual(5, Demo1Field.D)

    def test_is_valid(self):
        self.assertTrue(1 in Demo1Field)
        self.assertTrue(2 in Demo1Field)
        self.assertTrue(3 in Demo1Field)
        self.assertFalse(4 in Demo1Field)
        self.assertTrue(5 in Demo1Field)
        self.assertFalse(6 in Demo1Field)

    def test_get_display(self):
        self.assertEqual('VER', Demo1Field.get_value_display(1))
        self.assertIsNone(Demo1Field.get_value_display(4))
        self.assertEqual('d', Demo1Field.get_value_display(5))
        self.assertEqual('f', Demo1Field.get_value_display(8))
        self.assertEqual('G', Demo1Field.get_value_display(10))


class FieldChoicesNewAttrTestCase(unittest.TestCase):
    def test_text(self):
        self.assertListEqual(
            [1, 2, 3, 5, 8, 10],
            Demo1Field.values
        )
