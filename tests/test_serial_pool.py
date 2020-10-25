# coding=utf8

import unittest

from borax.counters.serial_pool import serial_no_generator, LabelFormatOpts, SerialNoPool


class SerialValueGeneratorTestCase(unittest.TestCase):
    def test_value_generator(self):
        self.assertEqual([0, 1, 2], list(serial_no_generator(upper=10))[:3])
        source = [0, 1, 2, 4, 5, 7]
        res = list(serial_no_generator(upper=10, values=source))[:2]
        self.assertListEqual([8, 9], res)
        res = list(serial_no_generator(upper=10, values=source))[:3]
        self.assertListEqual([8, 9, 3], res)
        res = list(serial_no_generator(upper=10, values=source))[:4]
        self.assertListEqual([8, 9, 3, 6], res)
        self.assertListEqual([9], list(serial_no_generator(reused=False, values=[7, 8]))[:4])


class LabelFormatOptsTestCase(unittest.TestCase):
    def test_invalid_opts(self):
        with self.assertRaises(ValueError):
            LabelFormatOpts('{no:02x}--{no:03d}')

    def test_basic(self):
        opts = LabelFormatOpts('LC{no}')
        self.assertEqual(2, opts.label2value('LC02'))
        self.assertEqual('LC02', opts.value2label(2))

    def test_hex_value(self):
        opts = LabelFormatOpts('FFFF{no:04X}')
        self.assertEqual(57159, opts.label2value('FFFFDF47'))
        self.assertEqual('FFFFDF47', opts.value2label(57159))

        opts2 = LabelFormatOpts('FFFF{no:04x}')
        self.assertEqual(57159, opts2.label2value('FFFFdf47'))
        self.assertEqual('FFFFdf47', opts2.value2label(57159))

        opts3 = LabelFormatOpts('FFFF{no}', base=16, digits=4)
        self.assertEqual(57159, opts3.label2value('FFFFdf47'))
        self.assertEqual('FFFFdf47', opts3.value2label(57159))


class SerialNoPoolTestCase(unittest.TestCase):
    def test_success_create(self):
        sp = SerialNoPool(lower=3, upper=5)
        self.assertEqual(3, sp.lower)
        self.assertEqual(5, sp.upper)

    def test_error_create(self):
        with self.assertRaises(ValueError):
            SerialNoPool(label_fmt='{no:02x}--{no:03d}')
        with self.assertRaises(ValueError):
            SerialNoPool(lower=-2)
        with self.assertRaises(ValueError):
            SerialNoPool(upper=-500)
        with self.assertRaises(ValueError):
            SerialNoPool(label_fmt='{no:02d}', lower=2, upper=1000)

    def test_basic_generate(self):
        sp = SerialNoPool()
        data = list(sp.get_next_generator())[:3]
        self.assertEqual(3, len(data))
        self.assertEqual(2, data[2].value)
        with self.assertRaises(TypeError):
            sp.generate(13)

    def test_custom_label_fmt(self):
        sp = SerialNoPool(label_fmt='X{no:01x}')
        data = sp.generate(16)
        self.assertListEqual(['Xc', 'Xd', 'Xe', 'Xf'], data[-4:])
        data = sp.generate_values(16)
        self.assertListEqual([12, 13, 14, 15], data[-4:])

    def test_data_manage(self):
        sp = SerialNoPool(label_fmt='LC{no:04d}')
        sp.add_elements([0, 1, 2, 3])
        data = sp.generate_labels(2)
        self.assertListEqual(['LC0004', 'LC0005'], data)
        sp.add_elements(data)
        sp.remove_elements([5])
        data = sp.generate_labels(2)
        self.assertListEqual(['LC0005', 'LC0006'], data)

        with self.assertRaises(ValueError):
            sp.add_elements([-2])
        with self.assertRaises(TypeError):
            sp.add_elements([2.5])
