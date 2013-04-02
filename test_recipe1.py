#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="TestBier"

m = Mash()
m.ingredient(Ingredient('grain','belgian pilsner','9.75lb'))
m.ingredient(Ingredient('grain','caravienne','1.25lb'))
m.ingredient(Ingredient('grain','candy sugar','0.87lb'))
m.ingredient('water','','5.0gal')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('boil_start_volume','6.5gal')
s.property('wort_volume','6.0gal')
s.solve()
r.add(s)

b = Recipe()
b.subname = "boil"
b.ingredient(Ingredient('hops','stryian goldings','1oz'))
b.ingredient(Ingredient('hops','stryian goldings','1oz'))
b.ingredient(Ingredient('misc','irish moss','1tsp'))
r.add(b)

f = Recipe()
f.subname = "ferment"
f.ingredient(Ingredient('yeast','white labs WLP550 belgian ale','1vial'))
f.ingredient(Ingredient('hops','stryian goldings','2oz'))
r.add(f)

print r


