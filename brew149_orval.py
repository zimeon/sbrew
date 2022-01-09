#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Orval-ish Brett Beer"

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'pilsener (briess)', '10.0lb', color='1.2L')
m.ingredient('grain', 'caravienne (briess)', '1.25lb', color='20L')
m.ingredient('water', 'strike', '5.5gal')
m.ingredient('misc', 'gypsum', '14g')
m.property('temp', '152F')
m.property('t_mashtun', '60F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.25gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time = Quantity('90min')
b.ingredient('hops', 'hallertau', '25IBU', time='60min', aa='4.0%AA')
b.ingredient('hops', 'styrian goldings', '1oz', time='15min', aa='3.5%AA')
b.ingredient('hops', 'styrian goldings', '1oz', time='0min', aa='3.5%AA')
b.ingredient('misc', 'irish moss', '1tsp', time='15min')
b.ingredient('sucrose', 'table sugar', '1.0lb', time='5min')
b.property('boil_end_volume', '6.5gal')
b.solve()
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'WLP510 Belgian Bastogne Ale', '1pack')
f.ingredient('yeast', 'WY5112 Brett Brux (after racking)', '1pack')
f.ingredient('hops', 'styrian goldings', '1oz', time='0min', aa='3.5%AA')
f.property('atten', '80.0%atten')
r.add(f)

r.solve()
print(r)
