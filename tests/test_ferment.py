"""Test code for sbrew.ferment"""

import unittest
from sbrew.quantity import Quantity
from sbrew.recipe import Recipe
from sbrew.ferment import Ferment


class TestAll(unittest.TestCase):

    def test_01_init(self):
        f = Ferment()
        self.assertEqual(f.name, 'Ferment')
        f = Ferment(name='my_fermentation')
        self.assertEqual(f.name, 'my_fermentation')

    def test_02_import_forward(self):
        ri = Recipe()
        ri.property('OG', Quantity('1.099', 'sg'))
        f = Ferment(start=ri)
        # self.assertEqual( f.property('OG', default=None), None )
        f.import_forward()
        self.assertEqual(str(f.property('OG').quantity), '1.099 sg')
        ri.property('OG', Quantity('1.001', 'sg'))
        f.import_forward()
        self.assertEqual(str(f.property('OG').quantity), '1.001 sg')

    def test_03_import_backward(self):
        f = Ferment()
        ro = Recipe(start=f)
        self.assertEqual(f.property('FG', default=None), None)
        ro.property('FG', Quantity('1.011', 'sg'))
        f.import_backward()
        self.assertEqual(str(f.property('FG').quantity), '1.011 sg')
        ro.property('FG', Quantity('1.005', 'sg'))
        f.import_backward()
        self.assertEqual(str(f.property('FG').quantity), '1.005 sg')

    def test04_solve_og_fg(self):
        f = Ferment()
        f.property('OG', Quantity('1.050', 'sg'))
        f.property('FG', Quantity('1.010', 'sg'))
        f.solve()
        self.assertEqual(str(f.property('ABV').quantity), '5.3 %ABV')
        self.assertEqual(str(f.property('atten').quantity), '80.0 %atten')

    def test05_solve_og_atten(self):
        f = Ferment()
        f.property('OG', Quantity('1.050', 'sg'))
        f.property('atten', Quantity('80.0', '%atten'))
        f.solve()
        self.assertEqual(str(f.property('ABV').quantity), '5.3 %ABV')
        self.assertEqual(str(f.property('FG').quantity), '1.010 sg')

    def test06_abv(self):
        # trivial spot-test of formula
        f = Ferment()
        f.property('OG', Quantity('1.050', 'sg'))
        f.property('FG', Quantity('1.010', 'sg'))
        self.assertAlmostEqual(f.abv(), 5.25)
        f.property('OG', Quantity('1.100', 'sg'))
        self.assertAlmostEqual(f.abv(), 11.8125)

    def test07_end_state_str(self):
        f = Ferment()
        self.assertEqual(f.end_state_str(), '?')
        f.property('ABV', Quantity('6.3', '%ABV'))
        self.assertEqual(f.end_state_str(), '6.3 %ABV')
        f.property('atten', Quantity('76', '%atten'))
        self.assertEqual(f.end_state_str(), '6.3 %ABV (76.0 %atten)')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
