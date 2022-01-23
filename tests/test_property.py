"""Test code for sbrew.property"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property


class TestAll(unittest.TestCase):

    def test01_init(self):
        p1 = Property('temp', '122F')
        self.assertEqual(p1.name, 'temp')
        self.assertAlmostEqual(p1.quantity.value, 122.0)
        self.assertEqual(p1.quantity.unit, 'F')
        p2 = Property('temp', 123.2, 'F')
        p3 = Property('temp', Quantity('124F'))
        p4 = Property('temp', Property('othertemp', '125F'))  # take Quantity from supplied Property
        p5 = Property('temp', '126F', therm2='a', therm1='b')

    def test02_to(self):
        self.assertAlmostEqual(Property('weight', '1.5lb').to('oz'), 24.0)

    def test03_short_str(self):
        self.assertEqual(Property('time', '1h').short_str(), '1.0 h')
        self.assertEqual(Property('temp', '124F').short_str(), 'temp 124.0 F')

    def test04_str(self):
        self.assertRegex(str(Property('water', '1gal')), r'water\s+1.00 gal')
        p5 = Property('temp', '126F', therm2='a', therm1='b')
        self.assertRegex(str(p5), r'temp\s+126.0 F\s+\( b\s+, a\s+\)')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
