#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Czech Pils"

m = InfusionMash()
m.ingredient('grain','american pilsener','9.0lb')
m.ingredient('grain','carapils','0.75lb')
m.ingredient('water','strike','4.84gal')
m.property('temp','154F')
m.property('t_mashtun','65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
#s.property('v_boil','6.5gal')
s.property('wort_volume','6.5gal')
s.solve()
r.add(s)

b = Boil()
b.time=Quantity('60min')
b.property('wort_volume','6.0gal')
b.ingredient('hops','simcoe','1.35oz',time=Quantity('60min'),aa=Quantity('13%'))
b.ingredient('hops','cascade','1oz',time=Quantity('30min'),aa=Quantity('3.2%'))
b.ingredient('hops','centennial','1oz',time=Quantity('10min'),aa=Quantity('9.9%'))
b.ingredient('hops','simcoe','0.65oz',time=Quantity('0min'),aa=Quantity('13%'))
r.add(b)

f = Ferment()
f.ingredient('yeast','wyeast 1056 American Ale','2vial')
r.add(f)

print r


