"""Test code for sbrew.step_mash"""

import unittest
from sbrew.step_mash import StepMash

class TestAll(unittest.TestCase):

    def test_01_init(self):
        sm = StepMash()
        self.assertEqual( sm.name, 'step_mash' )
        sm = StepMash(name='my_step_mash')
        self.assertEqual( sm.name, 'my_step_mash' )

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

