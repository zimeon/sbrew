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

    def test01_extractions_calculated_forward(self):
        # v_water, v_in_grain, v_wort
        bs = BatchSparge()
        # set dead volume to 0.0
        bs.v_dead = Quantity('0.0gal')
        #bs.extracts = 2 #assumed
        self.assertEqual( bs.extractions_calculated_forward(1.0,0,1.0), ([1.0,0.0],[1.0,0.0]) )
        self.assertEqual( bs.extractions_calculated_forward(2.0,1.0,1.0), ([1.0,0.0],[0.5,0.0]) )
        self.assertEqual( bs.extractions_calculated_forward(2.0,1.0,2.0), ([1.0,1.0],[0.5,0.25]) )
        (vols, points) = bs.extractions_calculated_forward(4.0,0.5,7.0)
        self.assertEqual( len(vols), 2 )
        self.assertAlmostEqual( vols[0], 3.5 )
        self.assertAlmostEqual( vols[1], 3.5 )
        self.assertAlmostEqual( points[0], 0.875 )
        self.assertAlmostEqual( points[1], 0.109375 )
        bs.v_dead = Quantity('0.5gal')
        self.assertEqual( bs.extractions_calculated_forward(2.0,0.5,1.0), ([1.0,0.0],[0.5,0.0]) )
        self.assertEqual( bs.extractions_calculated_forward(2.0,0.5,2.0), ([1.0,1.0],[0.5,0.25]) )
        # 3-way batch sparge
        bs.extracts = 3
        bs.v_dead = Quantity('0.0gal')
        (vols, points) = bs.extractions_calculated_forward(2.0,1.0,2.0)
        self.assertEqual( len(vols), 3 )
        self.assertAlmostEqual( vols[0], 1.0 )
        self.assertAlmostEqual( vols[1], 0.5 )
        self.assertAlmostEqual( vols[2], 0.5 )
        self.assertAlmostEqual( points[0], 0.5 )
        self.assertAlmostEqual( points[1], 0.16666666 )
        self.assertAlmostEqual( points[2], 0.11111111 )
        # 4-way batch sparge
        bs.extracts = 4
        bs.v_dead = Quantity('0.0gal')
        (vols, points) = bs.extractions_calculated_forward(2.0,1.0,4.0)
        self.assertEqual( len(vols), 4 )
        self.assertAlmostEqual( vols[0], 1.0 )
        self.assertAlmostEqual( vols[1], 1.0 )
        self.assertAlmostEqual( vols[2], 1.0 )
        self.assertAlmostEqual( vols[3], 1.0 )
        self.assertAlmostEqual( points[0], 0.5 )
        self.assertAlmostEqual( points[1], 0.25 )
        self.assertAlmostEqual( points[2], 0.125 )
        self.assertAlmostEqual( points[3], 0.0625 )
        # 5-way batch sparge
        bs.extracts = 5
        bs.v_dead = Quantity('0.0gal')
        (vols, points) = bs.extractions_calculated_forward(2.0,1.0,5.0)
        self.assertEqual( len(vols), 5 )
        self.assertAlmostEqual( vols[0], 1.0 )
        self.assertAlmostEqual( vols[1], 1.0 )
        self.assertAlmostEqual( vols[2], 1.0 )
        self.assertAlmostEqual( vols[3], 1.0 )
        self.assertAlmostEqual( vols[4], 1.0 )
        self.assertAlmostEqual( points[0], 0.5 )
        self.assertAlmostEqual( points[1], 0.25 )
        self.assertAlmostEqual( points[2], 0.125 )
        self.assertAlmostEqual( points[3], 0.0625 )
        self.assertAlmostEqual( points[4], 0.03125 )
  
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
        self.assertAlmostEqual( bs.property('wort_gravity').to('sg'), 1.043712797 )
        # 'grain','water','total_points','boil_start_volume'
        bs = BatchSparge()
        bs.v_dead = Quantity('0.25gal')
        bs.grain_water_retention = Quantity('0.55qt/lb') # qt/lb
        bs.property('grain',Quantity('10lb'))
        bs.property('water',Quantity('4gal'))
        bs.property('total_points',Quantity('300points'))
        bs.property('boil_start_volume',Quantity('6.5gal'))
        bs.solve()
        self.assertAlmostEqual( bs.property('wort_gravity').to('sg'), 1.040854933 )

    def test03_solve_from_mash_and_desired_volume(self):
        bs = BatchSparge()
        self.assertRaises( MissingParam, bs.solve_from_mash_and_desired_volume )
        bs.property('boil_start_volume','6gal')
        bs.property('water','5gal')
        bs.property('grain','8lb')
        bs.property('total_points','300points')
        bs.solve_from_mash_and_desired_volume()
        self.assertAlmostEqual( bs.property('wort_gravity').quantity.value, 1.04507432 )
        self.assertAlmostEqual( bs.property('wort_volume').quantity.value, 6.00 )

