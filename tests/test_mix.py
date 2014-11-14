"""Test code for sbrew.mix"""

import unittest

from sbrew.mix import mix_two_temp

class TestAll(unittest.TestCase):

    def test00_mix_two_temp(self):
        # same temp
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,1.0,1.0), 1.0 )
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,1.0,0.0), 1.0 )
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,1.0,1000.0), 1.0 )
        # zero hc
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,10000.0,0.0), 1.0 )
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,1.0,0.0), 1.0 )
        # equal hc
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,3.0,1.0), 2.0 )
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,1000.0,1.0), 500.5 )
        # diff hc
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,5.0,3.0), 4.0 )
        self.assertAlmostEqual( mix_two_temp(1.0,1.0,1002.0,0.001), 2.0 )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
