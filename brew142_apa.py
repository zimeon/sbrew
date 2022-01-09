#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "American Pale Ale - Cascade & Centennial for Amanda & Joe"

# ithaca water, plus
# 15g gypsum in 12gal strike water
# w = Water()
# w.ingredient('gypsum','','12g')

m = InfusionMash()
m.ingredient('grain', 'Marris Otter', '10lb', color='4L')
m.ingredient('grain', 'Pale Wheat', '0.5lb', color='4L')
m.ingredient('water', 'strike', '5.25gal')
m.property('temp', '150F')
m.property('t_mashtun', '76F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'Centennial', '1.0oz', time='60min', aa='8.1%AA')
b.ingredient('hops', 'Cascade', '1.5oz', time='5min', aa='5.4%AA')
b.ingredient('hops', 'Cascade', '1.0oz', time='1min', aa='5.4%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Safbrew S-05', '1pack')
# f.property('OG','1.050sg')
f.property('atten', '80%atten')
r.add(f)

r.solve()
print(r)
