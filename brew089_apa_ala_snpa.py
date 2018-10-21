#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "American Pale Ale in the mold of Sierra Nevada"

# refs:
# http://byo.com/recipe-exchange/item/3025-sierra-nevada-pale-ale-clone
# OG=1.052, 37IBU, 9% crystal 40L, 150mash
#

# ithaca water

m = InfusionMash()
m.ingredient('grain', '2 row', '10.0lb', color='2L')
m.ingredient('grain', 'Crystal 55', '1.25lb', color='55L')
m.ingredient('water', 'strike', '5.0gal')
m.property('temp', '152F')
m.property('t_mashtun', '63F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'Perle', '1.0oz', time='60min', aa='7.5%AA')
b.ingredient('hops', 'Perle', '0.75oz', time='30min', aa='7.5%AA')
b.ingredient('hops', 'Cascade', '1.0oz', time='10min', aa='6.5%AA')
b.ingredient('hops', 'Cascade', '1.0oz', time='0min', aa='6.5%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Safbrew S-05', '1pack/starter')
# f.property('OG','1.050sg')
f.property('atten', '80%atten')
r.add(f)

r.solve()
print(r)
