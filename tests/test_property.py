"""Test code for sbrew/property"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property

class TestAll(unittest.TestCase):

    def test_str(self):
        self.assertRegexpMatches( str(Property('water','1gal')), r'water\s+1.00 gal')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

