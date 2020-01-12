"""Test code for sbrew/quantity"""

import unittest

from sbrew.quantity import Quantity, ConversionError


class TestAll(unittest.TestCase):

    def test01_parse(self):
        self.assertEqual(Quantity("50F").value, 50.0)
        self.assertEqual(Quantity("50F").unit, "F")
        self.assertEqual(Quantity("1.2lb").value, 1.2)
        self.assertEqual(Quantity("1.lb").value, 1.0)
        self.assertEqual(Quantity("1lb").value, 1.0)

    def test02_parse_value(self):
        self.assertEqual(Quantity("0").value, 0.0)
        self.assertEqual(Quantity("2").value, 2.0)
        self.assertEqual(Quantity("2.0").value, 2.0)
        self.assertEqual(Quantity("2.5").value, 2.5)
        self.assertEqual(Quantity("2.000001").value, 2.000001)

    def test03_find_conversion(self):
        self.assertAlmostEqual(Quantity.find_conversion('g', 'kg'), 0.001)
        self.assertAlmostEqual(Quantity.find_conversion('kg', 'g'), 1000.0)
        self.assertAlmostEqual(Quantity.find_conversion('lb', 'oz'), 16.0)
        self.assertAlmostEqual(Quantity.find_conversion('oz', 'lb'), 1.0 / 16.0)
        self.assertAlmostEqual(Quantity.find_conversion('%', 'fraction'), 0.01)

    def test04_str(self):
        self.assertEqual(str(Quantity(unit='%ABV')), '? %ABV')
        self.assertEqual(str(Quantity("1.23")), '1.23 (dimensionless)')
        self.assertEqual(str(Quantity("1.013sg")), '1.013 sg')
        self.assertEqual(str(Quantity("1.01345sg")), '1.013 sg')
        self.assertEqual(str(Quantity("1.35%")), '1.4 %')

    def test05_repr(self):
        self.assertEqual(repr(Quantity(unit='%ABV')), 'QuantityNotDefined')
        self.assertEqual(repr(Quantity("1.2345")), '1.2345')
        self.assertEqual(repr(Quantity("1.0134sg")), '1.0134sg')

    def test06_canonical_unit(self):
        self.assertEqual(Quantity.canonical_unit('hour'), 'h')

    def test07_to(self):
        self.assertAlmostEqual(Quantity('1lb').to('oz'), 16.0)
        self.assertAlmostEqual(Quantity('30min').to('hour'), 0.5)
        self.assertAlmostEqual(Quantity('32F').to('C'), 0.0)
        self.assertAlmostEqual(Quantity('-18C').to('F'), -0.4)

    def test08_temp_to(self):
        self.assertAlmostEqual(Quantity('32F').temp_to('C'), 0.0)
        self.assertAlmostEqual(Quantity('-18C').temp_to('F'), -0.4)
        # expect exception for non temperature input or output unit
        q = Quantity('1C')
        self.assertRaises(ConversionError, q.temp_to, 'kg')
        q = Quantity('1.001sg')
        self.assertRaises(ConversionError, q.temp_to, 'F')

    def test09_convert_to(self):
        self.assertAlmostEqual(Quantity('1lb').convert_to('oz').value, 16.0)
        self.assertEqual(Quantity('1lb').convert_to('oz').unit, 'oz')
        self.assertAlmostEqual(Quantity('1lb').convert_to('oz').value, 16.0)
        self.assertEqual(Quantity('30min').convert_to('hour').unit, 'h')

    def test10_add(self):
        q1 = Quantity('1lb') + Quantity('1oz')
        self.assertAlmostEqual(q1.value, 1.0625)
        self.assertEqual(q1.unit, 'lb')
        q2 = Quantity('1oz') + Quantity('1lb')
        self.assertAlmostEqual(q2.value, 17)
        self.assertEqual(q2.unit, 'oz')

    def test11_sub(self):
        q1 = Quantity('1lb') - Quantity('1oz')
        self.assertAlmostEqual(q1.value, 0.9375)
        self.assertEqual(q1.unit, 'lb')
        q2 = Quantity('19oz') - Quantity('1lb')
        self.assertAlmostEqual(q2.value, 3)
        self.assertEqual(q2.unit, 'oz')

    def test12_mul(self):
        q1 = Quantity('1lb') * 1.23
        self.assertAlmostEqual(q1.value, 1.23)
        self.assertEqual(q1.unit, 'lb')
        q1 = Quantity('1%') * 2  # integer
        self.assertAlmostEqual(q1.value, 2)
        self.assertEqual(q1.unit, '%')

    def test12_rmul(self):
        # Multiply should also work the other way around
        q1 = 2.34 * Quantity('1lb')
        self.assertAlmostEqual(q1.value, 2.34)
        self.assertEqual(q1.unit, 'lb')

    def test20_find_conversion(self):
        self.assertEqual(Quantity.find_conversion('xyz', 'xyz'), 1.0)
        self.assertAlmostEqual(Quantity.find_conversion('g', 'kg'), 0.001)
        # error conditions
        self.assertRaises(ConversionError, Quantity.find_conversion, 'xyz', 'lb')
        self.assertRaises(ConversionError, Quantity.find_conversion, 'lb', 'xyz')
        self.assertRaises(ConversionError, Quantity.find_conversion, 'lb', 'h')

    def test21_hydrometer_correction(self):
        q = Quantity('1.010sg')
        self.assertAlmostEqual(q.hydrometer_correction().to('sg'), 1.010)
        q = Quantity('1.010sg')
        self.assertAlmostEqual(q.hydrometer_correction('100F').to('sg'), 1.016)
        q = Quantity('1.010sg')
        self.assertAlmostEqual(q.hydrometer_correction('118F').to('sg'), 1.020)

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
