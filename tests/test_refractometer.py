"""Test code for sbrew/refractometer"""

import unittest

from sbrew.quantity import Quantity
from sbrew.refractometer import brix_to_starting_gravity


class TestAll(unittest.TestCase):

    def test_01_brix_to_starting_gravity(self):
        self.assertAlmostEqual(brix_to_starting_gravity(Quantity(0, 'Brix')).to('sg'), 1.0, places=4)
        self.assertAlmostEqual(brix_to_starting_gravity(Quantity(5, 'Brix')).to('sg'), 1.020, places=3)
        self.assertAlmostEqual(brix_to_starting_gravity(Quantity(10, 'Brix')).to('sg'), 1.040, places=3)
        self.assertAlmostEqual(brix_to_starting_gravity(Quantity(15, 'Brix')).to('sg'), 1.061, places=3)
        self.assertAlmostEqual(brix_to_starting_gravity(Quantity(20, 'Brix')).to('sg'), 1.083, places=3)

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
