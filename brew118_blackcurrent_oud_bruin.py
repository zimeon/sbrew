#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Blackcurrant Oud Bruin"
r.description = """Based on brew #99, and Oud Bruin inspired by
<http://www.themadfermentationist.com/2011/01/sour-brown-barrel-day-3.html>
(or p312 of the "American Sour Beers" book). After a clean fermentation
will add Roeselare yeastm, blackcurrents and Bourbon soaked oak chips."""

# ithaca water

m = InfusionMash()
m.ingredient('grain', 'marris otter', '12lb', color='4L')  # T-F Marris Otter
m.ingredient('grain', 'dark munich', '2lb', color='15L')  # Avangard Malz (German) 15L
m.ingredient('grain', 'crystal 120L', '8oz', color='120L')  # Briess Caramel(Crystal) 120L
m.ingredient('grain', 'biscuit', '8oz', color='22L')  # Dingemans Biscuit 18-27L, sub for Melanoidin 30L
m.ingredient('grain', 'chocolate', '4oz', color='400L')  # Simpson's Chocolate
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
