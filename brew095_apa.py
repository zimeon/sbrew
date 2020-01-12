#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "American Pale Ale with fresh hops from and for Liz & Pete"

# ithaca water, plus
# 15g gypsum in 12gal strike water
# w = Water()
# w.ingredient('gypsum','','12g')

m = InfusionMash()
# oops, should have been 10lb
m.ingredient('grain', '2-row', '8.5lb', color='2L')
# http://www.midwestsupplies.com/maillard-malts-briess-munich-malt-10l.html
m.ingredient('grain', 'Munich', '0.5lb', color='10L')
m.ingredient('grain', 'Crystal 55', '0.5lb', color='55L')
m.ingredient('water', 'strike', '5.25gal')
m.property('temp', '150F')
m.property('t_mashtun', '63F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('dme', 'muntons extra light', '1.50lb', time='15min')
b.ingredient('hops', 'Perle', '1.25oz', time='60min', aa='7.5%AA')
b.ingredient('hops', 'Cascade (whole)', '1.0oz', time='30min', aa='4%AA')
b.ingredient('hops', 'Cascade (whole)', '1.0oz', time='10min', aa='4%AA')
b.ingredient('hops', 'Cascade (whole)', '1.0oz', time='5min', aa='4%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Safbrew S-05', '1pack')
# f.property('OG','1.050sg')
f.property('atten', '80%atten')
r.add(f)

r.solve()
print(r)
