#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Brown Porter"

m = InfusionMash()
m.ingredient('grain','american 2-row','10.75lb')
m.ingredient('grain','marris otter','2.0lb')
m.ingredient('grain','crystal 55','0.25lb')
m.ingredient('water','strike','5.3gal')
m.property('temp','152F')
m.property('t_mashtun','65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('v_boil','6.5gal')
s.property('wort_volume','6.0gal')
s.solve()
r.add(s)

b = Recipe()
b.subname = "boil"
b.time=Quantity('60min')
b.ingredient('hops','stryian goldings','1oz',time=Quantity('60min'))
b.ingredient(Ingredient('hops','stryian goldings','1oz',time=Quantity('15min')))
b.ingredient(Ingredient('misc','irish moss','1tsp',time=Quantity('15min')))
r.add(b)

f = Recipe()
f.subname = "ferment"
f.ingredient('yeast','white labs WLP001 California ale','1vial')
r.add(f)

print r


