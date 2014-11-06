"""Test code for beer"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.beer import Beer

class TestAll(unittest.TestCase):

    def test00_str(self):
        b = Beer()
        self.assertEqual( str(b), '= beer =\n')
        self.assertEqual( b.end_state_str(), '')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

