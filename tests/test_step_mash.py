"""Test code for sbrew.step_mash"""

import unittest
from sbrew.step_mash import StepMash
from sbrew.recipe import Recipe

class TestAll(unittest.TestCase):

    def test_01_init(self):
        sm = StepMash()
        self.assertEqual( sm.name, 'step mash' )
        sm = StepMash(name='my_step_mash')
        self.assertEqual( sm.name, 'my_step_mash' )

    def test02_add_step(self):
        sm = StepMash()
        self.assertEqual( len(sm.steps), 0)
        sm.add_step(type="infuse",volume="2gal",temp="122F")
        self.assertEqual( len(sm.steps), 1 )
        sm.add_step(type="rest",time="10min")
        self.assertEqual( len(sm.steps), 2 )
        sm.add_step(type="heat",temp="212F")
        self.assertEqual( len(sm.steps), 3 )
        sm.add_step(type="adjust")
        self.assertEqual( len(sm.steps), 4 )
        sm.add_step(type="boil")
        self.assertEqual( len(sm.steps), 5 )
        self.assertRaises( Exception, sm.add_step, "unknown_type" )

    def test_03_total_water(self):
        r = Recipe()
        r.property('total_water', '1gal')
        sm = StepMash(start=r)
        self.assertAlmostEqual(sm.total_water().to('gal'), 1.0)
        sm.add_step(type="infuse",volume="2gal",temp="122F")
        self.assertAlmostEqual(sm.total_water().to('gal'), 3.0)
        sm.add_step(type="infuse",volume="0.5gal",temp="162F")
        self.assertAlmostEqual(sm.total_water().to('gal'), 3.5)

    def test_04_total_time(self):
        sm = StepMash()
        sm.add_step(type="rest",time="10min")
        self.assertAlmostEqual( sm.total_time().total_seconds(), 600.0 )
        sm.add_step(type="rest",time="1min")
        self.assertAlmostEqual( sm.total_time().total_seconds(), 660.0 )

    def test_05_steps_str(self):
        sm = StepMash()
        sm.add_step(type="infuse",volume="2gal",temp="122F")
        sm.add_step(type="rest",time="10min")
        sm.add_step(type="heat",temp="212F")
        sm.add_step(type="adjust")
        sm.add_step(type="boil")
        self.assertRegexpMatches( sm.steps_str(), r'0:00:00 \| rest -> 2.00 gal @ 122.0 F' )
        self.assertRegexpMatches( sm.steps_str(), r'0:10:00 \| heat -> 2.00 gal @ 122.0 F' )
        self.assertRegexpMatches( sm.steps_str(), r'0:10:00 \| adjust -> 2.00 gal @ 212.0 F' )
        self.assertRegexpMatches( sm.steps_str(), r'0:10:00 \| state -> 2.00 gal @ 212.0 F' )

    def test_06_stage_state_str(self):
        sm = StepMash()
        stage = { 'type':'type_here', 'volume':'vol_here', 'temp': 'temp_here' }
        self.assertEqual( sm.stage_state_str(stage), 'type_here -> vol_here @ temp_here ' )

    def test_07_find_stages(self):
        sm = StepMash()
        sm.add_step(type="infuse",volume="2gal",temp="122F")
        sm.add_step(type="rest",time="10min")
        sm.add_step(type="heat",temp="212F")
        sm.add_step(type="adjust")
        sm.add_step(type="boil")
        stages={}
        sm.find_stages(stages, mash_name='abc')
        self.assertEqual( len(stages['abc']), 5 )
        # last stage
        self.assertEqual( stages['abc'][4]['type'], 'state' )
        self.assertEqual( stages['abc'][4]['time'].total_seconds(), 600.0 )

    def test_08_parsetime(self):
        sm = StepMash()
        self.assertEqual( sm.parsetime('1h').total_seconds(), 3600.0 )

    def test_09_str(self):
        sm = StepMash()
        sm.add_step(type="infuse",volume='1gal',temp='123F')
        sm.add_step(type="rest",time="10min")
        self.assertRegexpMatches( str(sm), r'= step mash =' )
        self.assertRegexpMatches( str(sm), r'\*\*\*steps\*\*\*' )
        self.assertRegexpMatches( str(sm), r'rest -> 1.00 gal @ 123.0 F' )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

