#!/usr/bin/env python
"""Run various scripts and check output to provide end-to-end tests"""

import sys
import subprocess
import unittest
from cStringIO import StringIO

class TestAll(unittest.TestCase):

    def run_script(self,script):
        """ Run script, collect stdout and check exit code 0 """
        p = subprocess.Popen([sys.executable,script],
                             stdout=subprocess.PIPE)
        self.assertEqual( p.wait(), 0 )
        return p.stdout.read()
        
        
    def test056(self):
        out = self.run_script('brew056_complete_breakfast.py')
        self.assertRegexpMatches( out, r'Gimme leftist' )
        # FIXME - no signifcant calculatio in 056

    def test058(self):
        p = subprocess.Popen([sys.executable,"brew058_tarrangon_belgian.py"],
                             stdout=subprocess.PIPE)
        #(child_stdout, child_stdin) = (p.stdout, p.stdin))
        self.assertEqual( p.wait(), 0 )
        out = p.stdout.read()
        self.assertRegexpMatches( out, r'requires 35.5 psi CO2' )

    def test060(self):
        out = self.run_script('brew060_loganberry_stout.py')

    def test065(self):
        out = self.run_script('brew065_hoppy_yum_ipa.py')

    def test065(self):
        out = self.run_script('brew066_czech_pils.py')

    def test065(self):
        out = self.run_script('brew068_wheat_wine_2.py')

    def test065(self):
        out = self.run_script('brew069_special_rye_bitter.py')

    def test065(self):
        out = self.run_script('brew070_oaked_smoked_brown_ale.py')

    def test065(self):
        out = self.run_script('brew071_robust_porter.py')

    def test065(self):
        out = self.run_script('brew076_dark_but_mild.py')

    def test065(self):
        out = self.run_script('brew077_gpa.py')

    def test065(self):
        out = self.run_script('brew078_saison.py')

    def test065(self):
        out = self.run_script('brew079_saison_fonce_avec_poivre.py')
        self.assertRegexpMatches( out, r'-> 6.00 gal @ 1.056 sg with 32.3 IBU')
        self.assertRegexpMatches( out, r'-> 6.8 %ABV \(91.1 %atten\)')

    def test080(self):
        out = self.run_script('brew080_hefe.py')
        self.assertRegexpMatches( out, r'-> 5.50 gal @ 1.050 sg with 14.0 IBU')

    def test081(self):
        out = self.run_script('brew081_wit_kk.py')
        self.assertRegexpMatches( out, r'-> 5.50 gal @ 1.050 sg with 17.2 IBU')

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
