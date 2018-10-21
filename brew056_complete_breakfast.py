#!/usr/bin/env python
from sbrew import *

r = Recipe()
r.name = "Complete Breakfast Brew#56"

m1 = InfusionMash(name='oatmeal pre-mash')
m1.ingredient(Ingredient('grain', 'oatmeal', '1.5lb'))
m1.ingredient(Ingredient('water', '', '1.1gal'))
m1.property('temp', '122F')
m1.property('duration', '30min')
r.add(m1)

m2 = InfusionMash(start=m1, name='main mash')
m2.ingredient(Ingredient('grain', 'marris otter', '8.0lb'))
m2.ingredient(Ingredient('grain', 'crystal 55', '1.0lb'))
m2.ingredient(Ingredient('grain', 'british chocolate (simpsons)', '0.75lb'))
m2.ingredient(Ingredient('grain', 'roast', '0.25lb'))
m2.ingredient(Ingredient('water', 'strike', '3.98gal'))
m2.property('temp', '152F')
m2.property('duration', '60min')
r.add(m2)

s = BatchSparge(start=m2)
s.property('wort_volume', '6.5gal')
r.add(s)

b = Boil(start=s)
b.property('boil_start_volume', '6.5gal')
b.property('boil_end_volume', '6.0gal')
b.ingredient(Ingredient('hops', 'stryian goldings', '1oz'))
b.ingredient(Ingredient('hops', 'stryian goldings', '1oz'))
b.ingredient(Ingredient('misc', 'irish moss', '1tsp'))
r.add(b)

f = Ferment(start=b)
f.ingredient(Ingredient('yeast', 'white labs WLP013 London Ale', '1cake'))
r.add(f)

c = Recipe(start=f, name="post-fermentation addition")
c.ingredient(Ingredient('coffee', 'Gimme leftist espresso', '800ml'))
r.add(c)

r.solve()
print(r)
