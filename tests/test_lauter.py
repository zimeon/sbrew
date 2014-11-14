"""Test code for sbrew.lauter"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.lauter import Lauter
from sbrew.recipe import Recipe

class TestAll(unittest.TestCase):

    def test01_init(self):
        l = Lauter()
        self.assertEqual( l.name, 'lauter' )
        l = Lauter(name="whatever")
        self.assertEqual( l.name, 'whatever' )

    def test02_import_forward(self):
        r = Recipe()
        r.property('total_grain', '10lb' )
        r.property('total_water', '6.5gal' )
        r.property('total_points', '333points' )
        l = Lauter(start=r)
        l.import_forward()
        self.assertAlmostEqual( l.property('grain').to('lb'), 10.0 )
        self.assertAlmostEqual( l.property('water').to('gal'), 6.5 )
        self.assertAlmostEqual( l.property('total_points').to('points'), 333.0 )

    def test03_import_forward(self):
        l = Lauter()
        l.import_backward() #empty

    def test04_solve(self):
        l = Lauter()
        self.assertRaises( Exception, l.solve )

    def test05_end_state_str(self):
        l = Lauter()
#        self.assertEqual( str(l), '= lauter =\n')
#        self.assertEqual( l.end_state_str(), '')
        l.property('wort_volume', '12.3gal')
        l.property('wort_gravity', '1.099sg')
        self.assertEqual( l.end_state_str(), '12.30 gal wort at 1.099 sg')
        l.extra_info = 'hi mum'
        self.assertRegexpMatches( l.end_state_str(), '1.099 sg\s+\(hi mum\)' )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

