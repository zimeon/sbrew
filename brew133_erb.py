#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Extra Rye Bitter (ERB)"

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'Marris Otter (TF)', '1.25lb', color='4L')
m.ingredient('grain', '2-row (Briess)', '4.0lb', color='2L')
m.ingredient('grain', 'Rye (TF)', '3.0lb', color='2.5L')
m.ingredient('grain', 'Munich (Weyermann)', '8oz', color='6L')
m.ingredient('grain', 'Wheat Malt (CM)', '1lb', color='2L')
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
b.ingredient('hops', 'Centennial', '0.7oz', time='60min', aa='8.4%AA')
b.ingredient('hops', 'Fuggles', '1.5oz', time='15min', aa='5.3%AA')
b.ingredient('hops', 'Fuggles', '1.0oz', time='0min', aa='5.3%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'WLP023 Butron Ale', '1pack')  # PurePitch Package
f.property('FG', '1.012sg')
r.add(f)

r.solve()
print(r)
