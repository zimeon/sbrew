"""Test code for sbrew.carbonation"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.carbonation import Carbonation
from sbrew.recipe import Recipe

class TestAll(unittest.TestCase):

    def test00_str(self):
        c = Carbonation()
        self.assertEqual( str(c), '= carbonation =\n')
        self.assertEqual( c.end_state_str(), '')

    def test01_import_forward(self):
        c = Carbonation()
        r = Recipe()
        self.assertFalse( c.has_property('ABV') )
        self.assertFalse( c.has_property('FG') )
        r.property('ABV',Quantity('5.0%ABV'))
        r.property('FG',Quantity('1.010sg'))
        c.connect_input(r)
        self.assertEqual( str(c.property('ABV').quantity), '5.0 %ABV' )
        self.assertEqual( str(c.property('FG').quantity), '1.010 sg' )

    def test02_solve(self):
        c = Carbonation()
        c.solve()

    def test03_end_state_str(self):
        c = Carbonation()
        c.property('vol',Quantity('1.5'))
        c.property('temp',Quantity('40F'))
        c.property('pressure',Quantity('12psi'))
        self.assertEqual( c.end_state_str(), 'Carbonation: 1.5 (dimensionless) @ 40.0 F requires 12.0 psi CO2' )
        
# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
