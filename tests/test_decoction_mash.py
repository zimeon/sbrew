"""Test code for sbrew.decoction_mash"""

import unittest
from sbrew.decoction_mash import DecoctionMash
from sbrew.recipe import MissingParam
from sbrew.quantity import Quantity

class TestAll(unittest.TestCase):

    def test_01_init(self):
        dm = DecoctionMash()
        self.assertEqual( dm.name, 'decoction mash' )
        dm = DecoctionMash(name='my_deco')
        self.assertEqual( dm.name, 'my_deco' )

    def test_02_split_and_mix(self):
        dm = DecoctionMash()
        self.assertEqual( len(dm.steps), 0 )
        deco=dm.split(remove="40%")
        self.assertEqual( deco.name, "decoction" )
        self.assertEqual( len(dm.steps), 1 )
        dm.add_step('rest')
        self.assertEqual( len(dm.steps), 2 )
        # bad split
        self.assertRaises( MissingParam, DecoctionMash().split )
        # check ingredients split
        dm1 = DecoctionMash()
        dm1.ingredient('a','aa','1kg')
        dm1.ingredient('b','bb','1.5gal')
        deco1=dm1.split(remove="20%")
        self.assertAlmostEqual( dm1.ingredient('a','aa').to('kg'), 1.0 ) #FIX - should really split
        self.assertAlmostEqual( deco1.ingredient('a','aa').to('kg'), 0.2 )
        self.assertAlmostEqual( dm1.ingredient('b','bb').to('gal'), 1.5 ) #FIX - should really split
        self.assertAlmostEqual( deco1.ingredient('b','bb').to('gal'), 0.3 )

    def test_03_infuse(self):
        # FIXME - not sure that water infusions are handled properly
        # FIXME - for now just check that water in description is right
        dm = DecoctionMash()
        dm.ingredient( 'grain', 'pilsner', '5lb' )
        dm.ingredient( 'water', 'strike', '5gal' )
        self.assertEqual( len(dm.steps), 0 )
        dm.add_step('rest', time="10min" )
        dm.add_step('infuse', volume=Quantity('1gal') )
        self.assertRegexpMatches( dm.steps_str(), r'0:10:00 | 6.39 gal' )
        self.assertEqual( len(dm.steps), 2 )
        dm.add_step('rest', time="10min" )
        dm.add_step('infuse', volume=Quantity('1gal') )
        self.assertEqual( len(dm.steps), 4 )
        self.assertRegexpMatches( dm.steps_str(), r'0:20:00 | 7.39 gal' )

    def test_04_str(self):
        dm = DecoctionMash()
        self.assertRegexpMatches( str(dm), r'= decoction mash =' )
        self.assertRegexpMatches( str(dm), r'\*\*\*steps\*\*\*' )

    def test_05_steps_str(self):
        dm = DecoctionMash()
        self.assertRegexpMatches( dm.steps_str(), r'0:00:00 | 0.00 gal @ QuantityNotDefined' )
        dm.add_step('rest',time='30min')
        deco =dm.split(remove="40%")
        deco.add_step('heat',temp='160F',time='15min')
        deco.add_step('rest',time='15min')
        deco.add_step('heat',temp='212F',time='15min')
        deco.add_step('boil',time='20min')
        dm.mix(deco)
        # should see two mashes in string
        self.assertRegexpMatches( dm.steps_str(), r'_main\s+|\s+decoction' )
        self.assertRegexpMatches( dm.steps_str(), r'-ditto-\s+\|\s+0.00 gal @ 160F' )

    def test_07_stage_state_str(self):
        dm = DecoctionMash()
        stage = {'volume': '1.1gal', 'temp': '134F'}
        self.assertRegexpMatches( dm.stage_state_str(stage), r'1.1gal @ 134F' )      

    def test_08_find_stages(self):
        dm = DecoctionMash()
        dm.add_step('rest',time='30min')
        dm.add_step('heat',temp='160F',time='15min')
        dm.add_step('rest',time='15min')
        dm.add_step('heat',temp='212F',time='15min')
        dm.add_step('boil',time='20min')
        stages={}
        dm.find_stages(stages)
        self.assertEqual( len(stages['_main']), 5 )
        self.assertEqual( stages['_main'][0]['type'], 'state' )
        self.assertEqual( stages['_main'][0]['time'].total_seconds(), 1800 )
        self.assertEqual( stages['_main'][1]['type'], 'state' )
        self.assertEqual( stages['_main'][1]['time'].total_seconds(), 2700 )
        self.assertEqual( stages['_main'][2]['type'], 'state' )
        self.assertEqual( stages['_main'][2]['time'].total_seconds(), 3600 )
        self.assertEqual( stages['_main'][3]['type'], 'state' )
        self.assertEqual( stages['_main'][3]['time'].total_seconds(), 4500 )
        self.assertEqual( stages['_main'][4]['type'], 'state' )
        self.assertEqual( stages['_main'][4]['time'].total_seconds(), 5700 )

    def test_10_total_time(self):
        dm = DecoctionMash()
        self.assertAlmostEqual( dm.total_time().total_seconds(), 0.0 )
        dm.add_step('rest',time='10min')
        self.assertAlmostEqual( dm.total_time().total_seconds(), 600.0 )
        dm.add_step('infuse',time='20min')
        self.assertAlmostEqual( dm.total_time().total_seconds(), 1800.0 )
 
# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

