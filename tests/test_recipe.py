"""Test code for sbrew.recipe"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.recipe import Recipe

class TestAll(unittest.TestCase):

    def test01_init(self):
        r = Recipe()
        self.assertEqual( r.name, None )
        self.assertEqual( r.verbose, False )
        self.assertEqual( r.debug, False )
        self.assertEqual( r.inputs, [] )
        r = Recipe(name="whatever")
        self.assertEqual( r.name, 'whatever' )

    def test02_connect_input(self):
        r1 = Recipe()
        r2 = Recipe(start=r1)
        self.assertEqual( r1.output, r2 )
        self.assertEqual( len(r2.inputs), 1 )
        self.assertEqual( r2.inputs[0], r1 )

    def test03_name_with_default(self):
        r = Recipe()
        self.assertEqual( r.name_with_default, 'recipe' )
        r.name = 'hi'
        self.assertEqual( r.name_with_default, 'hi' )
         
    def test04_fullname(self):
        r = Recipe()
        self.assertEqual( r.fullname, 'recipe' )
        r.name = 'hi'
        self.assertEqual( r.fullname, 'hi' )
 
    def test05_str(self):
        r = Recipe()
        self.assertEqual( str(r), '= recipe =\n' )
        r.ingredient('grain','special','10lb')
        self.assertRegexpMatches( str(r), r'Ingredients:\s+grain\s+special\s+10.0 lb' )
        r.property('heat','20C')
        self.assertRegexpMatches( str(r), r'Properties:\s+heat\s+20.0 C' )

    def test06_str_line_number(self):
        r = Recipe()
        kwargs = {}
        self.assertEqual( r._str_line_num(kwargs), '' )
        kwargs = {'line_number': 50}
        self.assertEqual( r._str_line_num(kwargs), '[051] ' )
        self.assertEqual( r._str_line_num(kwargs), '[052] ' )

    def test07__add__(self):
        r1 = Recipe()
        r1.ingredient('grain','pink','1oz')
        r2 = Recipe()
        r2.ingredient('grain','blue','2oz')
        r = r1 + r2
        self.assertEqual( len(r.ingredients), 2 )
        self.assertEqual( r.ingredients[0].name, 'pink' )
        self.assertEqual( r.ingredients[1].name, 'blue' )

    def test08_ingredient(self):
        pass

    def test09_property(self):
        pass
        
    def test10_has_properties(self):
        pass
        
    def test11_has_property(self):
        pass
        
    def test12_add(self):
        pass
        
    def test13_import_property(self):
        pass
        
    def test14_set_output(self):
        pass
        
    def test15_solve(self):
        r = Recipe()
        r.solve()
        r1 = Recipe()
        r.add(r1)
        r2 = Recipe()
        r.add(r2)
        r.solve()

    def test16_end_state_str(self):
        r = Recipe()
        self.assertEqual( r.end_state_str(), '' )

# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()

