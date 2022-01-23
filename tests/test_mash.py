"""Test code for sbrew.mash"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.mash import Mash
from sbrew.recipe import Recipe


class TestAll(unittest.TestCase):

    def test01_init(self):
        m = Mash()
        self.assertEqual(m.name, 'Mash')
        m = Mash(name='my mash')
        self.assertEqual(m.name, 'my mash')

    def test01_total_type(self):
        m = Mash()
        m.ingredient('grain', 'first grain', '1lb')
        m.ingredient('grain', 'second grain', '1kg')
        self.assertAlmostEqual(m.total_type('grain').to('lb'), 3.2046, places=4)
        m.ingredient('water', 'some water', '1gal')
        self.assertAlmostEqual(m.total_type('water').to('gal'), 1.0)
        m.ingredient('water', 'more water', '2gal')
        self.assertAlmostEqual(m.total_type('water').to('gal'), 3.0)

    def test02_total_grains(self):
        m1 = Mash()
        m1.ingredient('grain', 'first grain', '1lb')
        m1.ingredient('grain', 'second grain', '1kg')
        self.assertAlmostEqual(m1.total_grains().to('lb'), 3.2046, places=4)
        m2 = Mash()
        m2.ingredient('grain', 'first grain', '30%')
        m2.ingredient('grain', 'second grain', '30%')
        m2.ingredient('grain', 'third grain', '40%')
        self.assertAlmostEqual(m2.total_grains(total_mass=Quantity('10lb')).value, 10.0)
        self.assertEqual(m2.total_grains(total_mass=Quantity('10lb')).unit, 'lb')
        self.assertAlmostEqual(m2.ingredients[0].quantity.to('lb'), 3.0)
        self.assertAlmostEqual(m2.ingredients[1].quantity.to('lb'), 3.0)
        self.assertAlmostEqual(m2.ingredients[2].quantity.to('lb'), 4.0)

    def test03_total_points(self):
        # FIXME - dump implementation at present
        m = Mash()
        m.ingredient('grain', 'first grain', '1lb')
        m.ingredient('grain', 'second grain', '2lb')
        m.ingredient('grain', 'third grain', '3lb')
        self.assertAlmostEqual(m.total_points().to('points'), 210.66, places=4)

    def test04_color_units(self):
        m = Mash()
        self.assertAlmostEqual(m.total_water().value, 0.0)
        m.ingredient('water', 'strike', '1gal')
        self.assertAlmostEqual(m.color_units().to('MCU'), 0.0)
        m.ingredient('grain', 'first grain', '1lb', color='0L')
        self.assertAlmostEqual(m.color_units().to('MCU'), 0.0)
        m.ingredient('grain', 'crystal grain', '2lb', color='50L')
        self.assertAlmostEqual(m.color_units().to('MCU'), 100.0, places=4)
        m.ingredient('grain', 'dark grain', '0.1lb', color='500L')
        self.assertAlmostEqual(m.color_units().to('MCU'), 150.0, places=4)
        # divide by zero
        m.ingredients[0].quantity.value = 0.0
        self.assertAlmostEqual(m.total_water().to('gal'), 0.0)
        self.assertAlmostEqual(m.color_units().to('MCU'), 0.0, places=4)
        self.assertAlmostEqual(m.property('MCU').to('MCU'), 150.0, places=4)

    def test05_mash_volume(self):
        m = Mash()
        m.ingredient('water', 'strike', '4gal')
        m.ingredient('grain', 'grain', '10lb')
        self.assertAlmostEqual(m.mash_volume().to('gal'), 4.78125, places=4)

    def test05_add_mash(self):
        m = Mash()
        m.ingredient('water', 'strike', '4gal')
        m.ingredient('grain', 'grain', '10lb')
        m1 = Mash()
        m1.ingredient('water', 'strike', '2gal')
        m1.ingredient('grain', 'grain', '4lb')
        m.add_mash(m1)
        self.assertAlmostEqual(m.total_grains().to('lb'), 14.0)
        self.assertAlmostEqual(m.total_water().to('gal'), 6.0)

    def test06_solve(self):
        m = Mash()
        m.ingredient('water', 'strike', '4gal')
        m.ingredient('grain', 'grain1', '2lb')
        m.ingredient('grain', 'grain2', '6lb')
        m.solve()
        self.assertAlmostEqual(m.property('total_grain').to('lb'), 8.0)
        self.assertAlmostEqual(m.property('total_water').to('gal'), 4.0)
        self.assertAlmostEqual(m.property('total_points').to('points'), 280.88, places=4)

    def test07_end_state_str(self):
        m = Mash()
        m.ingredient('water', 'strike', '4gal')
        m.ingredient('grain', 'grain1', '2lb')
        m.ingredient('grain', 'grain2', '6lb')
        self.assertEqual(m.end_state_str(), 'total_grain 8.0 lb, total_water 4.00 gal, total_points 280.9 points')

    def test08_str(self):
        m = Mash()
        self.assertRegex(str(m), r'\sMash\s')
        self.assertRegex(str(m), r'total_grain 0.0 lb, total_water 0.00 gal, total_points 0.0 points')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
