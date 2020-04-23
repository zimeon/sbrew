#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "American Pale Ale with HBC586 Experimental Hop"

# HBC 586 is an aroma hop for whirlpool and dry hopping additions. It features intense notes of tropical fruit, mango, guava, citrus, herbal, and sulfur that are well suited for IPAs and hop-forward beers, including Wheat Ale, Golden Ale, American Lager, Pale Ales, India Pale Lager, India Pale Ale, Session IPA, New England IPA, and Imperial IPA styles.
# https://www.johnihaas.com/wp-content/uploads/2019/11/Haas-HopSpecSheets_HBC586-2018.pdf

# ithaca water, plus
# 15g gypsum in 12gal strike water

m = InfusionMash()
m.ingredient('grain', '2-row', '10lb', color='1.8L')
m.ingredient('grain', 'wheat', '0.5lb', color='2L')
m.ingredient('water', 'strike', '5.25gal')
m.property('temp', '150F')
m.property('t_mashtun', '66F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'Centennial', '25.0IBU', time='60min', aa='8.4%AA')
b.ingredient('hops', 'HBC586', '1.0oz', time='5min', aa='13.3%AA')
b.ingredient('hops', 'HBC586', '1.0oz', time='1min', aa='13.3%AA')
b.ingredient('misc', 'Irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'Safbrew S-05', '1pack')
f.property('atten', '80%atten')
r.add(f)

r.solve()
print(r)
