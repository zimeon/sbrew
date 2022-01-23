#!/usr/bin/env python

from sbrew import *

r = Recipe("Dubbel Trouble (collaboration with Tre)")

m = InfusionMash()
m.ingredient('grain', 'Pilsner malt (Weyermann)', '11lb', color='1.6L')
m.ingredient('grain', 'Munich malt (Weyermann)', '1lb', color='6L')
m.ingredient('grain', 'Aromatic malt', '0.5lb', color='20L')
m.ingredient('grain', 'CaraMunich malt (Briess)', '0.5lb', color='60L')
m.ingredient('grain', 'Special B malt (Dingemans)', '0.5lb', color='140L')
m.ingredient('water', 'strike', '5.5gal')
m.property('temp', '148F')
m.property('t_mashtun', '60F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s, duration="90min")
b.ingredient('hops', 'Tettnanger', '4oz', time='60min', aa='2.3%AA')
b.ingredient('hops', 'Saaz', '5IBU', time='60min', aa='3.6%AA')
b.ingredient('sucrose', 'Amber Belgian Candi Syrup', '1lb', time='0min', color='45L')
b.ingredient('sucrose', 'Table sugar', '8oz', time='0min', color='0L')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.description = "Start at 65F, raise to 70F over a week after start of action."
f.ingredient('yeast', 'wyeast 3787 trappist', '1packet')
f.property('atten', '80.0%atten')
r.add(f)

r.solve()
print(r)
