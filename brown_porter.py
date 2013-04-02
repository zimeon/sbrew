#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Brown Porter"

m = InfusionMash()
m.ingredient('grain','marris otter','7.0lb')
m.ingredient('grain','crystal 55','0.5lb')
m.ingredient('grain','brown malt','1.0lb')
m.ingredient('grain','british chocolate (simpsons)','0.5lb')
m.ingredient('water','strike','4.2gal')
m.property('temp','122F')
m.property('t_mashtun','70F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('boil_start_volume','6.5gal')
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


