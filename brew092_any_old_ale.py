#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Any Old Ale"

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'marris otter', '14.5lb', color='4L')
m.ingredient('grain', 'munich', '1.5lb', color='10L')
m.ingredient('grain', 'crystal 55', '12oz', color='55L')
m.ingredient('grain', 'crystal 120', '8oz', color='120L')
m.ingredient('grain', 'coffee', '4oz', color='150.0L')
m.ingredient('water', 'strike', '5.4gal')
m.property('temp', '150F')
m.property('t_mashtun', '68F')
r.add(m)

s = BatchSparge(start=m, extracts=3)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('90min')
b.ingredient('dme', 'muntons extra light', '0.5lb', time='15min')
b.ingredient('hops', 'centennial', '1.0oz', time='90min', aa='8.7%AA')
b.ingredient('hops', 'ekg', '2.0oz', time='90min', aa='6.5%AA')
b.ingredient('misc', 'irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'white labs WL001 cal ale', '1starter')
# f.property('ABV','8%ABV')
f.property('atten', '75%atten')
r.add(f)

r.solve()
print(r)
