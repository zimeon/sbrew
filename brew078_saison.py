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
m.property('temp', '148F')
m.property('t_mashtun', '60F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.5gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time = Quantity('90min')
b.ingredient('hops', 'amarillo', '0.75oz', time=Quantity('60min'),
             aa=Quantity('10.3%AA'))  # intended 0.9oz but forgot to fix
b.ingredient('hops', 'saaz', '0.50oz', time=Quantity(
    '0min'), aa=Quantity('3.2%AA'))
b.ingredient('misc', 'irish moss', '1tsp', time=Quantity('15min'))
b.ingredient('misc', 'gypsum', '5g')
b.ingredient('sucrose', 'table sugar', '1lb', time=Quantity('5min'))
b.property('boil_end_volume', '6.5gal')
b.solve()
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Wyeast 3711 French Saison', '1pack')
r.add(f)

print(r)
