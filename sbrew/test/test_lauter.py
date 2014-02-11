"""Test code for sbrew/lauter"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.lauter import Lauter

class TestAll(unittest.TestCase):

    def test_str(self):
        l = Lauter()
#        self.assertEqual( str(l), '= lauter =\n')
#        self.assertEqual( l.end_state_str(), '')
        l.property('wort_volume', '12.3gal')
        l.property('wort_gravity', '1.099sg')
        self.assertEqual( l.end_state_str(), '12.30 gal wort at 1.099 sg\n')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

