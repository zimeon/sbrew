#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "American Pale Ale for Amanda and Joe"

# ithaca water, plus
# 15g gypsum in 12gal strike water

m = InfusionMash()
m.ingredient('grain', '2-row', '10lb', color='1.8L')
m.ingredient('grain', 'Crystal 55', '1lb', color='55L')
m.ingredient('water', 'strike', '5.25gal')
m.property('temp', '150F')
m.property('t_mashtun', '63F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'Perle', '21.0IBU', time='60min', aa='7.0%AA')
b.ingredient('hops', 'Cascade', '10.0IBU', time='15min', aa='5.3%AA')
b.ingredient('hops', 'Cascade', '2.0oz', time='5min', aa='5.3%AA')
b.ingredient('misc', 'Irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Safbrew S-05', '1pack')
# f.property('OG','1.050sg')
f.property('atten', '80%atten')
r.add(f)

r.solve()
print(r)
