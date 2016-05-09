#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Robust Porter"

# Ithaca water

m = InfusionMash()
m.ingredient('grain','marris otter','11.0lb')
m.ingredient('grain','chocolate (Weyermann Carafa I)','1lb')
m.ingredient('grain','simpsons coffee','8oz')
m.ingredient('grain','crystal 55','8oz')
m.ingredient('water','strike','5.0gal')
m.property('temp','150F')
m.property('t_mashtun','65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
b.ingredient('hops','fuggles','1.5oz',time=Quantity('60min'),aa=Quantity('5%'))
b.ingredient('hops','willamette','0.75oz',time=Quantity('5min'),aa=Quantity('5%'))
b.ingredient('hops','willamette','0.75oz',time=Quantity('0min'),aa=Quantity('5%'))
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','wyeast 1318 English Ale III','1vial')
r.add(f)

print(r)


