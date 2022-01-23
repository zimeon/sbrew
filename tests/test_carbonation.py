"""Test code for sbrew.carbonation"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.carbonation import Carbonation
from sbrew.recipe import Recipe, MissingParam


class TestAll(unittest.TestCase):

    def test00_str(self):
        c = Carbonation()
        self.assertEqual(c.name, 'Carbonation')
        self.assertEqual(c.end_state_str(), '')

    def test01_import_forward(self):
        c = Carbonation()
        r = Recipe()
        self.assertFalse(c.has_property('ABV'))
        self.assertFalse(c.has_property('FG'))
        r.property('ABV', Quantity('5.0%ABV'))
        r.property('FG', Quantity('1.010sg'))
        c.connect_input(r)
        self.assertEqual(str(c.property('ABV').quantity), '5.0 %ABV')
        self.assertEqual(str(c.property('FG').quantity), '1.010 sg')

    def test02_solve(self):
        c1 = Carbonation()
        self.assertRaises(MissingParam, c1.solve)
        c1.property('temp', '45F')
        c1.property('pressure', '12psi')
        c1.property('vol', '2.0')
        c1.solve()
        # temp and pressure known
        c2 = Carbonation()
        c2.property('temp', '45F')
        c2.property('pressure', '12psi')
        c2.solve()
        self.assertAlmostEqual(c2.property('vol').quantity.value, 2.2537, places=4)
        # temp and vol known
        c3 = Carbonation()
        c3.property('temp', '45F')
        c3.property('vol', '2.0')
        c3.solve()
        self.assertAlmostEqual(c3.property('pressure').to('psi'), 9.0182, places=4)
        # pressure and vol known
        c4 = Carbonation()
        c4.property('pressure', '15psi')
        c4.property('vol', '2.0')
        c4.solve()
        self.assertAlmostEqual(c4.property('temp').to('F'), 58.09719, places=4)

    def test03_end_state_str(self):
        c = Carbonation()
        c.property('vol', Quantity('1.5'))
        c.property('temp', Quantity('40F'))
        c.property('pressure', Quantity('12psi'))
        self.assertEqual(c.end_state_str(), 'Carbonation: 1.5 (dimensionless) @ 40.0 F requires 12.0 psi CO2')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
