#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Extra Rye Bitter (ERB)"

# ithaca water

m = InfusionMash()
m.ingredient('grain', '2-row (Briess)', '4.0lb', color='2L')
m.ingredient('grain', 'Rye (Briess)', '3.0lb', color='3.7L')
m.ingredient('grain', 'Marris Otter (TF)', '1.5lb', color='4L')
m.ingredient('grain', 'Wheat Malt (CMC)', '1.25lb', color='2L')
m.ingredient('grain', 'Coffee (Simpsons)', '2oz', color='150L')
m.ingredient('water', 'strike', '5.0gal')
m.property('temp', '152F')
m.property('t_mashtun', '63F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
# boil
b.ingredient('hops', 'Cascade', '1.25oz', time='60min', aa='4.0%AA')
b.ingredient('hops', 'Cascase', '2.0oz', time='15min', aa='4.0%AA')
b.ingredient('hops', 'Cascase', '1.0oz', time='0min', aa='4.0%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'S-04 English Ale', '1pack')
f.property('FG', '1.012sg')
r.add(f)

r.solve()
print(r)
