# coding=utf8


import unittest

from borax import choices


class Demo1Field(choices.ConstChoices):
    A = 1, 'VER'
    B = 2, 'STE'
    c = 3, 'SSS'
    D = 5
    _E = 6, 'ES'
    F = 8
    G = choices.Item(10)


class FieldChoiceTestCase(unittest.TestCase):
    def test_get_value(self):
        self.assertEqual(1, Demo1Field.A)
        self.assertEqual(2, Demo1Field.B)
        self.assertEqual(5, Demo1Field.D)

    def test_is_valid(self):
        self.assertTrue(Demo1Field.is_valid(1))
        self.assertTrue(Demo1Field.is_valid(2))
        self.assertTrue(Demo1Field.is_valid(3))
        self.assertFalse(Demo1Field.is_valid(4))
        self.assertTrue(Demo1Field.is_valid(5))
        self.assertFalse(Demo1Field.is_valid(6))

    def test_get_display(self):
        self.assertEqual('VER', Demo1Field.get_value_display(1))
        self.assertIsNone(Demo1Field.get_value_display(4))
        self.assertEqual('5', Demo1Field.get_value_display(5))
        self.assertEqual('8', Demo1Field.get_value_display(8))
        self.assertEqual('10', Demo1Field.get_value_display(10))


class GenderChoices(choices.ConstChoices):
    MALE = choices.Item(1, 'Male')
    FEMALE = choices.Item(2, 'Female')
    UNKNOWN = choices.Item(3, 'Unknown')


class ChoicesItemTestCase(unittest.TestCase):
    def test_get_value(self):
        self.assertEqual(1, GenderChoices.MALE)

    def test_is_valid(self):
        self.assertTrue(GenderChoices.is_valid(1))
        self.assertTrue(GenderChoices.is_valid(2))
        self.assertTrue(GenderChoices.is_valid(3))
        self.assertFalse(GenderChoices.is_valid(4))

    def test_get_display(self):
        self.assertEqual('Male', GenderChoices.get_value_display(1))
        self.assertEqual('Female', GenderChoices.get_value_display(2))
        self.assertIsNone(Demo1Field.get_value_display(4))

    def test_get_names_and_values_and_labels(self):
        self.assertTupleEqual(('MALE', 'FEMALE', 'UNKNOWN'), GenderChoices.names)
        self.assertTupleEqual((1, 2, 3), GenderChoices.values)
        self.assertTupleEqual(('Male', 'Female', 'Unknown'), GenderChoices.displays)
        self.assertTupleEqual(('Male', 'Female', 'Unknown'), GenderChoices.labels)

    def test_choices(self):
        self.assertListEqual([(1, 'Male'), (2, 'Female'), (3, 'Unknown')], GenderChoices.choices)


class OffsetChoices(choices.ConstChoices):
    up = choices.Item((0, -1), 'Up')
    down = choices.Item((0, 1), 'Down')
    left = choices.Item((-1, 0), 'Left')
    right = choices.Item((0, 1), 'Right')


class OffsetChoicesTestCase(unittest.TestCase):
    def test_get_value(self):
        self.assertEqual((0, -1), OffsetChoices.up)

    def test_is_valid(self):
        self.assertTrue(OffsetChoices.is_valid((0, 1)))
        self.assertTrue(OffsetChoices.is_valid((-1, 0)))
        self.assertFalse(OffsetChoices.is_valid((0, 0)))
        self.assertFalse(OffsetChoices.is_valid(0))

    def test_get_display(self):
        self.assertEqual('Up', OffsetChoices.get_value_display((0, -1)))
        self.assertEqual('Left', OffsetChoices.get_value_display((-1, 0)))
        self.assertIsNone(OffsetChoices.get_value_display((0, 0)))


# --------- Class Inheritance ----------------------


class VerticalChoices(choices.ConstChoices):
    S = choices.Item('S', 'south')
    N = choices.Item('N', 'north')


class DirectionChoices(VerticalChoices):
    E = choices.Item('E', 'east')
    W = choices.Item('W', 'west')


class OrderTestChoices(VerticalChoices):
    N = choices.Item('n', 'North', order=-1)


class DirectionChoicesTestCase(unittest.TestCase):
    def test_child_class(self):
        self.assertEqual(2, len(VerticalChoices.choices))
        self.assertEqual(2, len(VerticalChoices))

        self.assertEqual(4, len(DirectionChoices.choices))
        self.assertEqual(4, len(DirectionChoices))

        expected = [('S', 'south'), ('N', 'north'), ('E', 'east'), ('W', 'west')]
        self.assertListEqual(expected, DirectionChoices.choices)
        self.assertListEqual(expected, list(DirectionChoices))

    def test_item_overwrite(self):
        self.assertEqual(2, len(OrderTestChoices.choices))
        self.assertEqual('n', OrderTestChoices.N)
        self.assertEqual('N', VerticalChoices.choices[1][0])
        self.assertEqual('n', OrderTestChoices.choices[0][0])
