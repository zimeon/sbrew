#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Oud Bruin Barrel Sour Collaboration"

# inspired by
# <http://www.themadfermentationist.com/2011/01/sour-brown-barrel-day-3.html>
# (or p312 of he American Sours book).

# ithaca water

m = InfusionMash()
m.ingredient('grain','marris otter','79.5%',color='4L')
m.ingredient('grain','dark munich','13%',color='9L')
m.ingredient('grain','crystal 90L','3%', color='90L')
m.ingredient('grain','melonoidin','3%', color='30L')
m.ingredient('grain','chocolate','1.5%', color='225L') #crisp
m.ingredient('water','strike','5.8gal')
m.property('total_grain','15lb')
m.property('temp','150F')
m.property('t_mashtun','68F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s, duration='60min')
b.ingredient('hops','amarillo','11IBU',time='60min',aa='8.2%AA')
b.ingredient('misc','irish moss','1tsp',time='15min')
b.property('boil_end_volume', '6.50gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','US-05 (Safale)','1pack')
#f.property('OG','1.069sg')
#f.property('ABV','8%ABV')
f.property('atten','80%atten')
r.add(f)

r.solve()
print r


