#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Oaked Smoked Brown Ale"

# ithaca water

m = InfusionMash()
m.ingredient('grain','marris otter','82%')
m.ingredient('grain','crystal 55L','6%')
m.ingredient('grain','crystal 120L','6%')
m.ingredient('grain','simpsons coffee','4%')
m.ingredient('grain','black patent','2%')
m.total_grains(Quantity('8lb'))
m.ingredient('water','strike','4.0gal')
m.property('temp','154F')
m.property('t_mashtun','65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
b.ingredient('hops','ekg','1.50oz',time=Quantity('60min'),aa=Quantity('5%'))
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.property('boil_end_volume', '6.5gal')
b.solve()
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','wyeast 1318 English Ale III','1vial')
r.add(f)

print r


