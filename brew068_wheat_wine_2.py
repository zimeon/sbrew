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
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.00gal')
r.add(s)

a = WortAdditions(start=s)
a.ingredient('ldme','muntons extra light','3lb')
a.ingredient('sucrose','table sugar','1.5lb')
r.add(a)

b = Boil(start=a)
b.time=Quantity('90min')
b.property('boil_end_volume','6.25gal')
b.ingredient('hops','hallertau','3oz',time=Quantity('90min'),aa=Quantity('3.9%AA'))
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','wyeast 1056 American Ale','2vial')
f.property('FG','1.024sg')
r.add(f)

r.solve()
print(r)


