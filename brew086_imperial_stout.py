#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Imperial Stout"

# ithaca water

m = InfusionMash()
m.ingredient('grain', '2-row (briess)', '14lb', color='4L')
m.ingredient('grain', 'special B', '1.0lb', color='65L')
m.ingredient('grain', 'coffee', '12oz', color='150.0L')
m.ingredient('grain', 'carafa I (weyermann)', '8oz', color='350.0L')
m.ingredient('grain', 'roast barley', '1.25lb', color='500L')
m.ingredient('water', 'strike', '4.7gal')
m.property('temp', '150F')
m.property('t_mashtun', '65F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('90min')
b.ingredient('dme', 'muntons extra light', '0.5lb', time='15min')
b.ingredient('hops', 'centennial', '0.5oz', time='60min', aa='9.9%AA')
b.ingredient('hops', 'cascade', '1.85oz', time='60min', aa='5.5%AA')
b.ingredient('hops', 'ekg', '2.0oz', time='60min', aa='7.2%AA')
b.ingredient('hops', 'fuggles', '1.0oz', time='10min', aa='4.6%AA')
b.ingredient('misc', 'irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'white labs WLP001 cal ale', '1starter')
# f.property('ABV','8%ABV')
f.property('atten', '75%atten')
r.add(f)

r.solve()
print(r)
