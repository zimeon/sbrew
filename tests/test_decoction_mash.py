"""Test code for sbrew.decoction_mash"""

import unittest
from sbrew.decoction_mash import DecoctionMash

class TestAll(unittest.TestCase):

    def test_01_init(self):
        dm = DecoctionMash()
        self.assertEqual( dm.name, 'decoction_mash' )
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
        dm.mix(deco)
        self.assertEqual( len(dm.steps), 3 )

    def test_04_total_water(self):
        pass

    def test_05_str(self):
        pass

    def test_06_steps_str(self):
        #,start_time=timedelta(),n=0,indent=''):
        pass

    def test_07_stage_state_str(self):
        pass

    def test_08_find_stages(self):
        #, stages, mash_name='_main', start_time=timedelta()):
        pass

    def test_09_parsetime(self):
        pass

    def test_10_total_time(self):
        pass

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

