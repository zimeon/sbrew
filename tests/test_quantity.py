"""Test code for sbrew/quantity"""

import unittest

from sbrew.quantity import Quantity,ConversionError

class TestAll(unittest.TestCase):

    def test01_parse(self):
        self.assertEqual( Quantity("50F").value, 50.0 )
        self.assertEqual( Quantity("50F").unit, "F" )
        self.assertEqual( Quantity("1.2lb").value, 1.2 )
        self.assertEqual( Quantity("1.lb").value, 1.0 )
        self.assertEqual( Quantity("1lb").value, 1.0 )

    def test02_parse_value(self):
        self.assertEqual( Quantity("0").value, 0.0 )
        self.assertEqual( Quantity("2").value, 2.0 )
        self.assertEqual( Quantity("2.0").value, 2.0 )
        self.assertEqual( Quantity("2.5").value, 2.5 )
        self.assertEqual( Quantity("2.000001").value, 2.000001 )

    def test03_find_conversion(self):
        self.assertAlmostEqual( Quantity.find_conversion('g','kg'), 0.001 )
        self.assertAlmostEqual( Quantity.find_conversion('kg','g'), 1000.0 )
        self.assertAlmostEqual( Quantity.find_conversion('lb','oz'), 16.0 )
        self.assertAlmostEqual( Quantity.find_conversion('oz','lb'), 1.0/16.0 )

    def test04_str(self):
        self.assertEqual( str(Quantity(unit='%ABV')), 'QuantityNotDefined' )
        self.assertEqual( str(Quantity("1.23")), '1.23 (dimensionless)' )
        self.assertEqual( str(Quantity("1.013sg")), '1.013 sg' )
        self.assertEqual( str(Quantity("1.01345sg")), '1.013 sg' )

    def test05_repr(self):
        self.assertEqual( repr(Quantity(unit='%ABV')), 'QuantityNotDefined' )
        self.assertEqual( repr(Quantity("1.2345")), '1.2345' )
        self.assertEqual( repr(Quantity("1.0134sg")), '1.0134sg' )

    def test06_canonical_unit(self):
        self.assertEqual( Quantity.canonical_unit('hour'), 'h' )
       
    def test07_to(self):
        self.assertAlmostEqual( Quantity('1lb').to('oz'), 16.0 )
        self.assertAlmostEqual( Quantity('30min').to('hour'), 0.5 )

    def test08_convert_to(self):
        self.assertAlmostEqual( Quantity('1lb').convert_to('oz').value, 16.0 )
        self.assertEqual( Quantity('1lb').convert_to('oz').unit, 'oz' )
        self.assertAlmostEqual( Quantity('1lb').convert_to('oz').value, 16.0 )
        self.assertEqual( Quantity('30min').convert_to('hour').unit, 'h' )

    def test09_add(self):
        q1 = Quantity('1lb')+Quantity('1oz')
        self.assertAlmostEqual( q1.value, 1.0625 )
        self.assertEqual( q1.unit, 'lb' )
        q2 = Quantity('1oz')+Quantity('1lb')
        self.assertAlmostEqual( q2.value, 17 )
        self.assertEqual( q2.unit, 'oz' )

    def test10_sub(self):
        q1 = Quantity('1lb')-Quantity('1oz')
        self.assertAlmostEqual( q1.value, 0.9375 )
        self.assertEqual( q1.unit, 'lb' )
        q2 = Quantity('19oz')-Quantity('1lb')
        self.assertAlmostEqual( q2.value, 3 )
        self.assertEqual( q2.unit, 'oz' )

    def test11_find_conversion(self):
        self.assertEqual( Quantity.find_conversion('xyz','xyz'), 1.0 )
        self.assertAlmostEqual( Quantity.find_conversion('g','kg'), 0.001 )
        # error conditions
        self.assertRaises( ConversionError, Quantity.find_conversion, 'xyz','F' )
        self.assertRaises( ConversionError, Quantity.find_conversion, 'F','xyz' )
        self.assertRaises( ConversionError, Quantity.find_conversion, 'F','sg' )

 
# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

