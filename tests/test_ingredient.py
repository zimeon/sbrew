"""Test code for sbrew.ingredient"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.ingredient import Ingredient

class TestAll(unittest.TestCase):

    def test00_init(self):
        i = Ingredient('grain','belgian pilsner','9.75lb')
        self.assertRegexpMatches( str(i), r'grain\s+belgian pilsner\s+9\.75 lb' )
        i2 = Ingredient('grain','belgian pilsner',9.75,'lb')
        self.assertRegexpMatches( str(i2), r'grain\s+belgian pilsner\s+9\.75 lb' )
        i3 = Ingredient('grain','us pilsner',Quantity(10.1,'lb'))
        self.assertRegexpMatches( str(i2), r'grain\s+us pilsner\s+10\.1 lb' )
        # pct
        i4 = Ingredient('grain','marris otter',pct=50.9)
        self.assertAlmostEqual( i4.pct, 50.9 )
        #self.assertEqual( str(i3.properties['temp2'].quantity), '133.0 F' )
        # Names properties
        i5 = Ingredient('grain','marris otter','5.4lb',temp=Quantity('144F') )
        self.assertEqual( str(i5.properties['temp'].quantity), '144.0 F' )

    def test01_str(self):
        i = Ingredient('grain','wheat malt','6.3lb',temp=Quantity('65F') )
        self.assertRegexpMatches( str(i), r'grain\s+wheat malt\s+6\.3 lb\s+\(temp 65\.0 F\)' )
        i2 = Ingredient('grain','belgian pilsner',pct=80.0,temp=Quantity("67F"))
        self.assertRegexpMatches( str(i2), r'grain\s+belgian pilsner\s+\( 80.0%\)\s+\(temp 67\.0 F\)' )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
