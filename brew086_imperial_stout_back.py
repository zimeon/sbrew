#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Imperial Stout"

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'marris otter', '80%', color='4L')
m.ingredient('grain', 'brown malt (crisp)', '10%', color='65L')
m.ingredient('grain', 'carafa I (weyermann)', '10%', color='350.0L')
m.ingredient('water', 'strike', '4.7gal')
m.property('temp', '150F')
m.property('t_mashtun', '65F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'ekg', '1.9oz', time=Quantity(
    '60min'), aa=Quantity('7.2%AA'))
b.ingredient('misc', 'irish moss', '1tsp', time=Quantity('15min'))
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'white labs WL001 cal ale', '1starter')
f.property('ABV', '8%ABV')
f.property('atten', '75%atten')
r.add(f)

r.solve()
print r
