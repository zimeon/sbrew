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
s.property('boil_start_volume','6.5gal')
s.property('wort_volume','6.0gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
b.ingredient('hops','simcoe','1.35oz',time=Quantity('60min'),aa=Quantity('13%AA'))
b.ingredient('hops','cascade','1oz',time=Quantity('30min'),aa=Quantity('3.2%AA'))
b.ingredient('hops','centennial','1oz',time=Quantity('10min'),aa=Quantity('9.9%AA'))
b.ingredient('hops','simcoe','0.65oz',time=Quantity('0min'),aa=Quantity('13%AA'))
b.ingredient('hops','cascade','0.5oz',time=Quantity('0min'),aa=Quantity('3.2%AA'))
b.ingredient('hops','centennial','0.5oz',time=Quantity('0min'),aa=Quantity('9.9%AA'))
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.property('boil_end_volume', '6gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','wyeast 1056 American Ale','2vial')
r.add(f)

r.solve()
print(r)


