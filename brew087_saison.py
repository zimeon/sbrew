#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Saison"

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'pilsener', '6.0lb')
m.ingredient('grain', 'wheat', '3.0lb')
m.ingredient('grain', 'munich', '0.75lb')
m.ingredient('water', 'strike', '5.0gal')
m.ingredient('misc', 'gypsum', '11g')
m.property('temp', '148F')
m.property('t_mashtun', '60F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.25gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('90min')
b.ingredient('hops', 'amarillo', '1.0oz',
             time=Quantity('60min'), aa=Quantity('8.2%AA'))
b.ingredient('hops', 'saaz', '0.50oz', time=Quantity(
    '0min'), aa=Quantity('3.6%AA'))
b.ingredient('misc', 'irish moss', '1tsp', time=Quantity('15min'))
b.ingredient('sucrose', 'table sugar', '1lb', time=Quantity('5min'))
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Danstar Belle Saison yeast', '2pack')
f.property('FG', '1.006sg')
r.add(f)

r.solve()
print(r)
