#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Random Oud Bruin"
r.description = """Based on brew #99, and Oud Bruin inspired by
<http://www.themadfermentationist.com/2011/01/sour-brown-barrel-day-3.html>
(or p312 of the "American Sour Beers" book). However, ingredients are a bit
random based on a limited selection at hand an now no brewing supply store in
town :-( After a clean initial fermentation with US-05 will add Roeselare
yeast in secondary and age for some time."""

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'marris otter', '12lb', color='4L')  # T-F Marris Otter
m.ingredient('grain', 'munich', '2lb', color='6L')
m.ingredient('grain', 'crystal 50-60L', '8oz', color='55L')
m.ingredient('grain', 'special b', '5oz', color='130L')
m.ingredient('grain', 'chocolate', '6oz', color='400L')  # Simpson's Chocolate
m.ingredient('water', 'strike', '4.5gal')
m.property('temp', '155F')
m.property('t_mashtun', '68F')
r.add(m)

s = BatchSparge(start=m, extracts=3)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s, duration='60min')
b.ingredient('hops', 'amarillo', '11IBU', time='60min', aa='8.2%AA')
b.ingredient('misc', 'irish moss', '1tsp', time='15min')
b.property('boil_end_volume', '6.50gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'US-05 (Safale)', '1pack')
# f.property('OG','1.069sg')
# f.property('ABV','8%ABV')
f.property('atten', '85%atten')
r.add(f)

r.solve()
print(r)
