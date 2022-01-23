"""Test code for beer"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.beer import Beer
from sbrew.recipe import Recipe


class TestAll(unittest.TestCase):

    def test00_str(self):
        b = Beer()
        self.assertEqual(str(b), '\n## Beer\n\n')
        self.assertEqual(b.end_state_str(), '')

    def test01_import_forward(self):
        b = Beer()
        r = Recipe()
        self.assertFalse(b.has_property('OG'))
        self.assertFalse(b.has_property('IBU'))
        self.assertFalse(b.has_property('ABV'))
        r.property('OG', Quantity('1.050sg'))
        r.property('IBU', Quantity('45IBU'))
        r.property('ABV', Quantity('5.0%ABV'))
        b.connect_input(r)
        self.assertEqual(str(b.property('OG').quantity), '1.050 sg')
        self.assertEqual(str(b.property('IBU').quantity), '45.0 IBU')
        self.assertEqual(str(b.property('ABV').quantity), '5.0 %ABV')

    def test02_solve(self):
        b = Beer()
        b.solve()

    def test03_end_state_str(self):
        b = Beer()
        b.property('ABV', Quantity('6.1%ABV'))
        self.assertEqual(b.end_state_str(), '6.1 %ABV')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
