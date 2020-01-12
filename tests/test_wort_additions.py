"""Test code for sbrew.wort_additions"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.wort_additions import WortAdditions
from sbrew.recipe import Recipe, MissingParam


class TestAll(unittest.TestCase):

    def test01_init(self):
        w = WortAdditions()
        self.assertEqual(w.name, 'wort additions')

    def test02_import_forward(self):
        r = Recipe()
        w = WortAdditions(start=r)
        self.assertFalse(w.has_property('wort_volume'))
        self.assertFalse(w.has_property('start_gravity'))
        self.assertFalse(w.has_property('MCU'))
        r.property('wort_volume', '7gal')
        r.property('wort_gravity', '1.070sg')
        r.property('MCU', '79MCU')
        w.import_forward()
        self.assertAlmostEqual(w.property('wort_volume').to('gal'), 7.0)
        self.assertAlmostEqual(w.property('start_gravity').to('sg'), 1.070)
        self.assertAlmostEqual(w.property('MCU').to('MCU'), 79.0)

    def test03_solve(self):
        w1 = WortAdditions()
        self.assertRaises(MissingParam, w1.solve)
        w1.property('wort_volume', '1.0gal')
        w1.property('start_gravity', '1.060sg')
        w1.ingredient('explicit', 'something', '1.0lb', ppg='46.0ppg')
        w1.solve()
        self.assertAlmostEqual(w1.property('wort_gravity').to('sg'), 1.106)
        w1.ingredient('sucrose', 'extra stuff', '8oz')
        w1.solve()
        self.assertAlmostEqual(w1.property('wort_gravity').to('sg'), 1.129)

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
