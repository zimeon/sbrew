"""Test code for sbrew/infusion_mash"""

import unittest

from sbrew.infusion_mash import InfusionMash
from sbrew.recipe import Recipe
from sbrew.ingredient import Ingredient
from sbrew.property import Property

class TestAll(unittest.TestCase):

    def test01_init(self):
        m = InfusionMash()

    def test02_import_forward(self):
        m1 = InfusionMash()
        m1.property('temp', '87F' )
        m1.property('hc_total', '123Btu/F')
        m1.ingredient('grain','marris otter','10lb')
        m2 = InfusionMash(start=m1)
        self.assertEqual( m2.property('t_initial').quantity.value, 87.0 )
        self.assertEqual( m2.total_grains().value, 10.0 )
        self.assertEqual( m2.total_water().value, 0.0 )
        m2.import_forward()
        self.assertEqual( m2.property('t_initial').quantity.value, 87.0 )
        self.assertEqual( m2.total_grains().value, 10.0 )
        self.assertEqual( m2.total_water().value, 0.0 )

    def test03_solve(self):
        m1 = InfusionMash()
        m1.property('temp', '87F' )
        m1.property('hc_initial', '123Btu/F')
        m1.property('t_initial', '67F')
        self.assertRaises( Exception, m1.solve )
        m1.ingredient('water','strike','4gal')
        m1.solve()
        self.assertAlmostEqual( m1.property('t_strike').to('F'), 163.875, places=3 )
        self.assertAlmostEqual( m1.property('hc_total').to('Btu/F'), 155.0, places=2 )
        self.assertAlmostEqual( m1.property('total_water').to('gal'), 4.0 )
        # start from mashtun and grain
        m2 = InfusionMash()
        m2.property('temp', '87F' )
        m2.property('hc_total', '123Btu/F')
        m2.ingredient('water','strike','4gal')
        m2.ingredient('grain','marris otter','10lb')
        m2.solve()
        self.assertAlmostEqual( m2.property('t_strike').to('F'), 91.1866, places=3 )
        self.assertAlmostEqual( m2.property('hc_total').to('Btu/F'), 36.962, places=2 )
        self.assertAlmostEqual( m2.property('total_water').to('gal'), 4.0 )


# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

