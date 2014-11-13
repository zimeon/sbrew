"""Test code for sbrew.mash"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.mash import Mash
from sbrew.recipe import Recipe

class TestAll(unittest.TestCase):

    def test00_str(self):
        m = Mash()
        self.assertEqual( m.name, 'mash' )
        self.assertEqual( m.end_state_str(), 'total_grain 0.0 lb, total_water 0.00 gal, total_points 0.0 points' )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
