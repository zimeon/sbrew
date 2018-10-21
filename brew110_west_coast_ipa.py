#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "American West Coast IPA"

# ithaca water

m = InfusionMash()
m.ingredient('grain', '2 row', '13.0lb', color='2L')
m.ingredient('grain', 'Caravienne', '0.5lb', color='20L')
m.ingredient('water', 'strike', '5.3gal')
m.property('temp', '150F')
m.property('t_mashtun', '62F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
# boil
b.ingredient('hops', 'Columbus', '2.0oz', time='60min', aa='14.1%AA')
b.ingredient('hops', 'Centennial', '2.0oz', time='60min', aa='8.5%AA')
b.ingredient('hops', 'Simcoe', '1.0oz', time='60min', aa='13.5%AA')
# mid
b.ingredient('hops', 'Columbus', '1.0oz', time='30min', aa='14.1%AA')
b.ingredient('hops', 'Simcoe', '1.0oz', time='15min', aa='13.5%AA')
b.ingredient('sucrose', 'table sugar', '1.0lb', time='5min')
# flame out
b.ingredient('hops', 'Centennial', '1.0oz', time='0min', aa='8.5%AA')
b.ingredient('hops', 'Simcoe', '1.0oz', time='0min', aa='13.5%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Safbrew US-05', '1yeast_cake')
# dry hop
f.ingredient('hops', 'Centennial', '1.0oz', aa='8.5%AA')
f.ingredient('hops', 'Simcoe', '1.0oz', aa='13.5%AA')
# f.property('OG','1.068',note="measured")
f.property('atten', '84%atten', note="84% from #090")
r.add(f)

r.solve()
print(r)
