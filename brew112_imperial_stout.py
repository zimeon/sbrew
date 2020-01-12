#!/usr/bin/env python
"""A recipe..."""
from sbrew import *

r = Recipe()
r.name = "Ithacan Imperial Stout"
r.description = (
    "Ithaca is not very Imperial in attitude, and so it is with this "
    "Imperial Stout that weighs in at only just approaching Imperial "
    "weight (about 8\% ABV). The goal is a well rounded chocolate "
    "and malty taste up front, revealing a roasty and slightly bitter "
    "finish without harshness or lingering hop taste.")

# ithaca water

m = InfusionMash()
m.ingredient('grain', '2-row (briess) malt', '14lb', color='1.8L')
m.ingredient('grain', 'special B malt', '1.0lb', color='65L')
m.ingredient('grain', 'coffee malt', '12oz', color='150.0L')
m.ingredient('grain', 'carafa I (weyermann) malt', '8oz', color='350.0L')
m.ingredient('grain', 'roast barley', '1.25lb', color='300L')
m.ingredient('water', 'strike', '5.0gal')
m.property('temp', '150F')
m.property('t_mashtun', '65F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('90min')
b.ingredient('dme', 'muntons extra light', '0.5lb', time='15min')
b.ingredient('hops', 'centennial', '61 IBU', time='60min', aa='10.4%AA')
b.ingredient('hops', 'fuggles', '1.0oz', time='10min', aa='4.6%AA')
b.ingredient('misc', 'irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Wyeast 1318 London Ale III', '1 yeast_cake')
# f.property('ABV','8%ABV')
f.property('atten', '75%atten')
r.add(f)

r.solve()
print(r)
# print(r.markdown_narrative())
