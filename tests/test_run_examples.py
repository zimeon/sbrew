#!/usr/bin/env python
"""Run various scripts and check output to provide end-to-end tests"""

from io import BytesIO
import subprocess
import sys
import unittest


class TestAll(unittest.TestCase):

    def run_script(self, script):
        """Run script, collect stdout and check exit code 0.

        Returns unicode string and not bytes.
        """
        p = subprocess.Popen([sys.executable, script],
                             stdout=subprocess.PIPE)
        self.assertEqual(p.wait(), 0)
        output = p.stdout.read()
        p.stdout.close()
        return(output.decode('utf-8'))

    def test056(self):
        out = self.run_script('brew056_complete_breakfast.py')
        self.assertRegex(out, r'Gimme leftist')
        # key outputs
        self.assertRegex(out, r'-> total_grain 11.5 lb, total_water 5.08 gal, total_points 403.8 points')
        self.assertRegex(out, r'-> 6.50 gal wort at 1.054 sg')
        self.assertRegex(out, r'-> 5.50 gal @ 1.059 sg with 26.7 IBU')

    def test058(self):
        out = self.run_script('brew058_tarrangon_belgian.py')
        # key outputs
        self.assertRegex(out, r' -> total_grain 10.5 lb, total_water 3.98 gal, total_points 368.7 points')
        self.assertRegex(out, r' -> 6.50 gal wort at 1.050 sg')
        self.assertRegex(out, r' -> 5.50 gal @ 1.054 sg with 55.7 IBU')
        self.assertRegex(out, r'requires 35.5 psi CO2')

    def test060(self):
        out = self.run_script('brew060_loganberry_stout.py')
        # check mash names
        self.assertRegex(out, r'\sfirst infusion\n')
        self.assertRegex(out, r'\ssecond infusion\n')
        self.assertRegex(out, r' -> 5.50 gal @ 1.051 sg with 42.2 IBU')

    def test065(self):
        out = self.run_script('brew065_hoppy_yum_ipa.py')
        # stats in output
        self.assertRegex(out, r'-> total_grain 13.0 lb, total_water 5.30 gal, total_points 456.4 points')
        self.assertRegex(out, r'-> 6.00 gal wort at 1.064 sg')
        self.assertRegex(out, r'-> 5.50 gal @ 1.064 sg with 60.2 IBU')

    def test066(self):
        out = self.run_script('brew066_czech_pils.py')

    def test068(self):
        out = self.run_script('brew068_wheat_wine_2.py')

    def test069(self):
        out = self.run_script('brew069_special_rye_bitter.py')

    def test070(self):
        out = self.run_script('brew070_oaked_smoked_brown_ale.py')

    def test071(self):
        out = self.run_script('brew071_robust_porter.py')

    def test076(self):
        out = self.run_script('brew076_dark_but_mild.py')

    def test077(self):
        out = self.run_script('brew077_gpa.py')

    def test078(self):
        out = self.run_script('brew078_saison.py')

    def test079(self):
        out = self.run_script('brew079_saison_fonce_avec_poivre.py')
        self.assertRegex(out, r'-> 6.00 gal @ 1.056 sg with 32.3 IBU')
        self.assertRegex(out, r'-> 6.8 %ABV \(91.1 %atten\)')

    def test080(self):
        out = self.run_script('brew080_hefe.py')
        # key outputs
        self.assertRegex(out, r'\sWarner Weisse\s\n')
        self.assertRegex(out, r'-> 5.50 gal @ 1.050 sg with 14.0 IBU')

    def test081(self):
        out = self.run_script('brew081_wit_kk.py')
        self.assertRegex(out, r'-> 5.50 gal @ 1.050 sg with 17.2 IBU')

    def test082(self):
        out = self.run_script('brew082_brown_porter.py')
        self.assertRegex(out, r'-> 6.00 gal @ 1.049 sg with 36.7 IBU')
        self.assertRegex(out, r'-> 4.9 %ABV \(75.5 %atten\)')

    def test086(self):
        out = self.run_script('brew086_imperial_stout.py')
        self.assertRegex(out, r'-> 8.1 %ABV \(75.0 %atten\)')

    def test087(self):
        out = self.run_script('brew087_saison.py')
        self.assertRegex(out, r'-> 6.00 gal @ 1.055 sg with 20.9 IBU')

    def test088(self):
        out = self.run_script('brew088_belgian_golden_barrel_sour_collab.py')
        self.assertRegex(out, r'-> 5.7 %ABV \(73.0 %atten\)')

    def test150(self):
        out = self.run_script('brew150_dubbel.py')
        self.assertRegex(out, r'IBU\s+27.2 IBU')  # this relies on counting sugars at end of boil
        self.assertRegex(out, r'-> 8.0 %ABV \(80.0 %atten\)')


# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
