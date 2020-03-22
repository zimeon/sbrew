#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Peak Saison (inspired by Apex Predator)"

# ithaca water, plus
# 15g gypsum in 12gal strike water

m = InfusionMash()
m.ingredient('grain', 'Pilsner (Weyermann)', '10.5lb', color='1.6L')
m.ingredient('grain', 'Wheat (Wyermann)', '1.5lb', color='2L')
m.ingredient('grain', 'Honey (Gambrinus)', '1lb', color='20L')
m.ingredient('water', 'strike', '5.25gal')
m.property('temp', '152F')
m.property('t_mashtun', '63F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'Crystal', '24.0IBU', time='60min', aa='4.5%AA')
b.ingredient('hops', 'Crystal', '10.0IBU', time='30min', aa='4.5%AA')
b.ingredient('hops', 'Crystal', '1.0oz', time='1min', aa='4.5%AA')
b.ingredient('hops', 'Sterling', '1.0oz', time='1min', aa='7.5%AA')
b.ingredient('misc', 'Irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Imperial B56 Rustic', '1pack')  # Alt for Wyeast 3726
# f.property('OG','1.050sg')
f.property('atten', '80%atten')
r.add(f)

r.solve()
print(r)
