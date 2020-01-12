#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Beer to solve for"

m = InfusionMash()
m.ingredient('grain', 'marris otter', '82%')
m.ingredient('grain', 'crystal 55L', '6%')
m.ingredient('grain', 'crystal 120L', '6%')
m.ingredient('grain', 'simpsons coffee', '4%')
m.ingredient('grain', 'black patent', '2%')
m.property('temp', '154F')
m.property('t_mashtun', '65F')
r.add(m)

s = BatchSparge(start=m)
r.add(s)

b = Boil(start=s)
b.ingredient('hops', 'fuggles', '1.00oz',
             time=Quantity('60min'), aa=Quantity('4.3%AA'))
b.ingredient('hops', 'cascade', '0.70oz',
             time=Quantity('60min'), aa=Quantity('3.2%AA'))
b.ingredient('misc', 'irish moss', '1tsp', time=Quantity('15min'))
b.property('duration', '60min')
b.property('boil_rate', '0.5gal/hour')
b.property('wort_volume', '6.0gal')
b.property('OG', '1.040sg')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'wyeast 1318 English Ale III', '1vial')
r.add(f)

r.solve()

print(r)
