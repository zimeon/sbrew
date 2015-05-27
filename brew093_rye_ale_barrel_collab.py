#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Rye Ale Barrel Sour Collaboration"

# inspired by
# <http://www.themadfermentationist.com/2011/03/rye-saison-with-brett.html>

# ithaca water

m = InfusionMash()
m.ingredient('grain','german pilsener','75%',color='2L')
m.ingredient('grain','rye malt','25%',color='10L')
m.ingredient('water','strike','5.7gal')
m.property('total_grain','15lb')
m.property('temp','150F')
m.property('t_mashtun','68F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s, duration='60min')
b.ingredient('hops','styrian goldings','2.5oz',time='60min',aa='5%AA')
b.ingredient('hops','styrian goldings','1.5oz',time='10min',aa='5%AA')
b.ingredient('misc','irish moss','1tsp',time='15min')
b.property('boil_end_volume', '6.50gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','saison yeast???','1starter')
#f.property('OG','1.070sg')
#f.property('ABV','8%ABV')
f.property('atten','80%atten')
r.add(f)

r.solve()
print r


