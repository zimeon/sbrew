"""Test code for sbrew.boil"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.boil import tinseth_utilization,ibu_from_boil,Boil
from sbrew.recipe import Recipe, MissingParam

class TestAll(unittest.TestCase):

    def test01_tinseth_utilization(self):
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.050sg'),Quantity('60min')), 0.230664077 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.050sg'),Quantity('600min')), 0.253677148 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.001sg'),Quantity('60min')), 0.35828726 )
        # Examples from Palmer, "How To Brew", 2006, p 58
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.040sg'),Quantity('15min')), 0.125, places=3 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.040sg'),Quantity('60min')), 0.252, places=3 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.040sg'),Quantity('90min')), 0.270, places=3 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.080sg'),Quantity('15min')), 0.087, places=3 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.080sg'),Quantity('60min')), 0.176, places=3 )
        self.assertAlmostEqual( tinseth_utilization(Quantity('1.080sg'),Quantity('90min')), 0.188, places=3 )

    def test02_ibu_from_boil(self):
        # Do calc from http://www.howtobrew.com/section1/chapter5-5.html
        ibu = ibu_from_boil(Quantity('1oz'),
                            Quantity('5%AA'),
                            Quantity('5gal'),
                            Quantity('1.050sg'),
                            Quantity('60min'))
        self.assertAlmostEqual( ibu, 17.2998, places=3 )

    def test03_init(self):
        b = Boil()
        self.assertEqual( b.name, 'boil' )
        b = Boil( 'my boil', '60min' )
        self.assertEqual( b.name, 'my boil' )
        self.assertAlmostEqual( b.property('duration').quantity.value, 60.0 )

    def test04_import_forward(self):
        r = Recipe()
        b = Boil(start=r)
        self.assertFalse( b.has_property('boil_start_volume') )
        self.assertFalse( b.has_property('start_gravity') )
        r.property('wort_volume','7gal')
        r.property('wort_gravity', '1.070sg')
        b.import_forward()
        self.assertAlmostEqual( b.property('boil_start_volume').to('gal'), 7.0 )
        self.assertAlmostEqual( b.property('start_gravity').to('sg'), 1.070 )

    def test05_solve(self):
        b1 = Boil()
        self.assertRaises( MissingParam, b1.solve )
        b1.property('boil_start_volume','6.5gal')
        b1.property('start_gravity','1.060sg')
        b1.property('boil_end_volume','6gal')
        b1.solve()
        self.assertAlmostEqual( b1.property('OG').to('sg'), 1.065 )
        self.assertAlmostEqual( b1.property('wort_volume').to('gal'), 5.5 )
        #
        b2 = Boil()
        b2.property('boil_start_volume','6.5gal')
        b2.property('start_gravity','1.060sg')
        b2.property('boil_rate','0.5gal/h')
        b2.property('duration','60min')
        b2.solve()
        self.assertAlmostEqual( b2.property('OG').to('sg'), 1.065 )
        self.assertAlmostEqual( b2.property('wort_volume').to('gal'), 5.5 )
        # add hops
        b2.ingredient('hops','cascade','2oz',time='60min',aa='4.5%AA')
        b2.solve()
        self.assertAlmostEqual( b2.property('IBU').to('IBU'), 22.677, places=3 )
        # backward
        b3 = Boil()
        b3.property('OG','1.065sg')
        b3.property('wort_volume','5.5gal')
        b3.property('boil_rate','0.5gal/h')
        b3.property('duration','60min')
        b3.solve()
        self.assertAlmostEqual( b3.property('boil_end_volume').to('gal'), 6.0 )
        self.assertAlmostEqual( b3.property('boil_start_volume').to('gal'), 6.5 )
        self.assertAlmostEqual( b3.property('start_gravity').to('sg'), 1.060 )

    def test08_points_from_sugars(self):
        b = Boil()
        self.assertEqual( b.points_from_sugars(), 0.0 )
        b.ingredient('sucrose','sugar1','10oz')
        self.assertAlmostEqual( b.points_from_sugars(), 28.75 )
        b.ingredient('sucrose','sugar2','10oz')
        self.assertAlmostEqual( b.points_from_sugars(), 57.5 )
        b.ingredient('maltose','sugar3', '1lb' ) # FIXME - add other sugars
        self.assertAlmostEqual( b.points_from_sugars(), 57.5 )
 
    def test09_ibu_from_addition(self):
        b = Boil()
        b.property('boil_end_volume','1gal')
        b.property('OG','1.040sg')
        self.assertAlmostEqual( b.ibu_from_addition( Quantity('1oz'), Quantity('1%AA'), Quantity('15min')),
                                9.3914, places=4 )
        self.assertAlmostEqual( b.ibu_from_addition( Quantity('10oz'), Quantity('1%AA'), Quantity('15min')),
                                93.914, places=2 )
        self.assertAlmostEqual( b.ibu_from_addition( Quantity('1oz'), Quantity('3%AA'), Quantity('90min')),
                                60.7383, places=2 )

    def test10_end_state_str(self):
        b = Boil()
        self.assertEqual( b.end_state_str(), '?' )
        b.property( 'wort_volume', '6gal' )
        self.assertEqual( b.end_state_str(), '6.00 gal' )
        b.property( 'OG', '1.056sg' )
        self.assertEqual( b.end_state_str(), '6.00 gal @ 1.056 sg' )
        b.property( 'IBU', '47IBU' )
        self.assertEqual( b.end_state_str(), '6.00 gal @ 1.056 sg with 47.0 IBU' )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

