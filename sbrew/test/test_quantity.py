"""Test code for sbrew/quantity"""

import unittest

from sbrew.quantity import Quantity

class TestAll(unittest.TestCase):

    def test_find_conversion(self):
        self.assertAlmostEqual( Quantity.find_conversion('g','kg'), 0.001 )
        self.assertAlmostEqual( Quantity.find_conversion('kg','g'), 1000.0 )
        self.assertAlmostEqual( Quantity.find_conversion('lb','oz'), 16.0 )
        self.assertAlmostEqual( Quantity.find_conversion('oz','lb'), 1.0/16.0 )


# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

