#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Wheat Wine II"

m = InfusionMash()
m.ingredient('grain','wheat matl','11.0lb')
m.ingredient('grain','marris otter','3.5lb')
m.ingredient('grain','chocolate','4oz')
m.ingredient('misc','rice hulls','4oz')
m.ingredient('water','strike','5.25gal')
m.property('temp','145F')
m.property('t_mashtun','65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','6.50gal')
s.solve()
r.add(s)

b = Recipe()
b.subname = "boil"
b.time=Quantity('60min')
b.property('wort_volume','6.0gal')
b.ingredient('hops','simcoe','1.35oz',time=Quantity('60min'),aa=Quantity('13%'))
b.ingredient('hops','cascade','1oz',time=Quantity('30min'),aa=Quantity('3.2%'))
b.ingredient('hops','centennial','1oz',time=Quantity('10min'),aa=Quantity('9.9%'))
b.ingredient('hops','simcoe','0.65oz',time=Quantity('0min'),aa=Quantity('13%'))
r.add(b)

f = Recipe()
f.subname = "ferment"
f.ingredient('yeast','wyeast 1056 American Ale','2vial')
r.add(f)

print r


