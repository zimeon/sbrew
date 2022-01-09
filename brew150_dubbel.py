#!/usr/bin/env python

from sbrew import *

r = Recipe("Dubbel Trouble (collaboration with Tre)")

m = InfusionMash()
m.ingredient('grain', 'Pilsner malt (Weyermann)', '11lb', color='1.6L')
m.ingredient('grain', 'Munich malt (Weyermann)', '1lb', color='6L')
m.ingredient('grain', 'Aromatic malt', '0.5lb', color='20L')
m.ingredient('grain', 'CaraMunich malt', '0.5lb', color='60L')
m.ingredient('grain', 'Special B malt', '0.5lb', color='120L')
m.ingredient('water', 'strike', '5.5gal')
m.property('temp', '148F')
m.property('t_mashtun', '60F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s, duration="90min")
b.ingredient('hops', 'Tettnanger', '27IBU', time='60min', aa='4%AA')
m.ingredient('sucrose', 'Amber Belgian Candi Syrup', '1lb', color='45L')
m.ingredient('sucrose', 'Table sugar', '8oz', color='0L')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'wyeast 3787 trappist', '1packet')
f.property('atten', '80.0%atten')
r.add(f)

r.solve()
print(r)
