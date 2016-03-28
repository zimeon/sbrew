#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Special Rye Bitter"

# water treatment
# 15g gypsum in 12gal strike water

m = InfusionMash()
m.ingredient('grain','marris otter','6.9lb')
m.ingredient('grain','rye','4.0lb')
m.ingredient('grain','crystal caravienne','9oz')
m.ingredient('grain','crystal 55','9oz')
m.ingredient('water','strike','5.65gal')
m.property('temp','152F')
m.property('t_mashtun','65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.5gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
b.ingredient('hops','fuggles','1.35oz',time=Quantity('60min'),aa=Quantity('5%AA'))
b.ingredient('hops','fuggles','0.8oz',time=Quantity('15min'),aa=Quantity('5%AA'))
b.ingredient('hops','fuggles','0.6oz',time=Quantity('2min'),aa=Quantity('5%AA'))
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.property('boil_end_volume', '7.0gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','wyeast 1318 English Ale III','1vial')
f.ingredient('water','dilute','1gal')
f.property('FG','1.014sg')
r.add(f)
r.solve()

print r


