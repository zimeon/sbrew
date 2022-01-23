"""Test code for sbrew.recipe"""

import unittest

from sbrew.quantity import Quantity
from sbrew.property import Property
from sbrew.recipe import Recipe, MissingParam


class TestAll(unittest.TestCase):

    def test01_init(self):
        r = Recipe()
        self.assertEqual(r.name, None)
        self.assertEqual(r.verbose, False)
        self.assertEqual(r.debug, False)
        self.assertEqual(r.inputs, [])
        r = Recipe(name="whatever")
        self.assertEqual(r.name, 'whatever')

    def test02_connect_input(self):
        r1 = Recipe()
        r2 = Recipe(start=r1)
        self.assertEqual(r1.output, r2)
        self.assertEqual(len(r2.inputs), 1)
        self.assertEqual(r2.inputs[0], r1)

    def test03_name_with_default(self):
        r = Recipe()
        self.assertEqual(r.name_with_default, 'recipe')
        r.name = 'hi'
        self.assertEqual(r.name_with_default, 'hi')

    def test04_fullname(self):
        r = Recipe()
        self.assertEqual(r.fullname, 'recipe')
        r.name = 'hi'
        self.assertEqual(r.fullname, 'hi')

    def test05_str(self):
        r = Recipe(name="MY-RECIPE")
        self.assertRegex(str(r), '\sMY-RECIPE\s')
        r.ingredient('grain', 'special', '10lb')
        self.assertRegex(str(r), r'Ingredients:\s+grain\s+special\s+10.0 lb')
        r.property('heat', '20C')
        self.assertRegex(str(r), r'Properties:\s+heat\s+20.0 C')

    def test06_str_line_number(self):
        r = Recipe()
        kwargs = {}
        self.assertEqual(r._str_line_num(kwargs), '')
        kwargs = {'line_number': 50}
        self.assertEqual(r._str_line_num(kwargs), '[051] ')
        self.assertEqual(r._str_line_num(kwargs), '[052] ')

    def test07__add__(self):
        r1 = Recipe()
        r1.ingredient('grain', 'pink', '1oz')
        r2 = Recipe()
        r2.ingredient('grain', 'blue', '2oz')
        r = r1 + r2
        self.assertEqual(len(r.ingredients), 2)
        self.assertEqual(r.ingredients[0].name, 'pink')
        self.assertEqual(r.ingredients[1].name, 'blue')

    def test08_ingredient(self):
        pass

    def test09_property(self):
        r = Recipe()
        r.property(Property('prop_a', '1.123sg'))
        self.assertAlmostEqual(r.properties['prop_a'].quantity.value, 1.123)
        r.property('prop_b', '1F')
        self.assertAlmostEqual(r.properties['prop_b'].quantity.value, 1.0)

    def test10_has_properties(self):
        pass

    def test11_has_property(self):
        pass

    def test12_properties_str(self):
        r = Recipe()
        r.property('prop_a', '1F')
        r.property('prop_b', '1.123sg')
        self.assertEqual(r.properties_str(), 'prop_a, prop_b')

    def test13_add(self):
        pass

    def test14_import_property(self):
        pass

    def test15_set_output(self):
        r = Recipe()
        r.set_output('abc')
        self.assertEqual(r.output, 'abc')
        self.assertRaises(Exception, r.set_output, 'def')

    def test16_solve(self):
        r = Recipe()
        r.solve()
        r1 = Recipe()
        r.add(r1)
        r2 = Recipe()
        r.add(r2)
        r.solve()

    def test17_end_state_str(self):
        r = Recipe()
        self.assertEqual(r.end_state_str(), '')

    def test101_missing_param(self):
        mp = MissingParam()
        self.assertEqual(str(mp), 'Missing parameter exception')
        mp = MissingParam('ooops')
        self.assertEqual(str(mp), 'ooops')


# If run from command line, do tests
if __name__ == '__main__':
    unittest.main()
