#!/usr/bin/env python

import sys
import subprocess
import unittest
from cStringIO import StringIO

class TestAll(unittest.TestCase):

#brew056_complete_breakfast.py

    def test058(self):
        p = subprocess.Popen([sys.executable,"brew058_tarrangon_belgian.py"],
                             stdout=subprocess.PIPE)
        #(child_stdout, child_stdin) = (p.stdout, p.stdin))
        self.assertEqual( p.wait(), 0 )
        out = p.stdout.read()
        self.assertRegexpMatches( out, r'requires 35.5 psi CO2' )

    def test060(self):
        p = subprocess.Popen([sys.executable,"brew060_loganberry_stout.py"])
        self.assertEqual( p.wait(), 0 )

#brew065_hoppy_yum_ipa.py
#brew066_czech_pils.py
#brew068_wheat_wine_2.py
#brew069_special_rye_bitter.py
#brew070_oaked_smoked_brown_ale.py
#brew071_robust_porter.py
#brew076_dark_but_mild.py
#brew077_gpa.py
#brew078_saison.py
#brew079_saison_fonce_avec_poivre.py

    def test080(self):
        p = subprocess.Popen([sys.executable,"brew080_hefe.py"])
        self.assertEqual( p.wait(), 0 )

    def test081(self):
        p = subprocess.call([sys.executable,"brew081_wit_kk.py"])
        self.assertEqual( p.wait(), 0 )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
