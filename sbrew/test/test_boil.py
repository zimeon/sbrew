"""Test code for sbrew/lauter"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.boil import Boil,ibu_from_boil

class TestAll(unittest.TestCase):

    def test_01palmer(self):
        # Do calc from http://www.howtobrew.com/section1/chapter5-5.html
        ibu = ibu_from_boil(Quantity('1oz'),
                            Quantity('5%AA'),
                            Quantity('5gal'),
                            Quantity('1.050SG'),
                            Quantity('60min'))
        self.assertAlmostEqual( ibu, 17.2998, places=3 )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

