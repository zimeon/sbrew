"""Test code for sbrew.batch_sparge"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.batch_sparge import BatchSparge
from sbrew.recipe import MissingParam

class TestAll(unittest.TestCase):

    def test00_str(self):
        bs = BatchSparge()
        self.assertEqual( str(bs), '= batch sparge =\n')
        self.assertEqual( bs.end_state_str(), '')

    def test01_extraction(self):
        #,v_boil,v_stuck,v_first):
        bs = BatchSparge()
        self.assertEqual( bs.extraction(2.0,0,1.0), (1.0,0.0,1.0) )
        self.assertEqual( bs.extraction(2.0,1.0,1.0), (0.5,0.25,1.0) )
        ( p_first, p_second, v_second ) = bs.extraction(2.0,99999999999.0,1.0)
        self.assertAlmostEqual( p_first, 0.0 )
        self.assertAlmostEqual( p_second, 0.0 )
        self.assertAlmostEqual( v_second, 1.0 )

    def test02_solve(self):
        bs = BatchSparge()
        bs.v_dead = Quantity('0.25gal')
        bs.grain_water_retention = Quantity('0.55qt/lb') # qt/lb
        self.assertRaises( MissingParam, bs.solve )
        # 'grain','water','total_points','wort_volume'
        bs.property('grain',Quantity('10lb'))
        bs.property('water',Quantity('4gal'))
        bs.property('total_points',Quantity('300points'))
        bs.property('wort_volume',Quantity('6gal'))
        bs.solve()
        self.assertAlmostEqual( bs.property('wort_gravity').to('sg'), 1.04378676 )
        # 'grain','water','total_points','boil_start_volume'
        bs = BatchSparge()
        bs.v_dead = Quantity('0.25gal')
        bs.grain_water_retention = Quantity('0.55qt/lb') # qt/lb
        bs.property('grain',Quantity('10lb'))
        bs.property('water',Quantity('4gal'))
        bs.property('total_points',Quantity('300points'))
        bs.property('boil_start_volume',Quantity('6.5gal'))
        bs.solve()
        self.assertAlmostEqual( bs.property('wort_gravity').to('sg'), 1.042319327 )

    def test03_solve_2(self):
        bs = BatchSparge()
        self.assertRaises( MissingParam, bs.solve_2 )
        bs.property('boil_start_volume','6gal')
        bs.property('water','5gal')
        bs.property('grain','8lb')
        bs.property('total_points','300points')
        bs.solve_2()
        self.assertAlmostEqual( bs.property('wort_gravity').quantity.value, 1.04651397 )
        self.assertAlmostEqual( bs.property('wort_volume').quantity.value, 5.75 )

    def test04_solve_from_mash_and_desired_volume(self):
        bs = BatchSparge()
        self.assertRaises( MissingParam, bs.solve_from_mash_and_desired_volume )
 

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

