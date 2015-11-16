#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Rye Ale Barrel Sour Collaboration"

# inspired by
# <http://www.themadfermentationist.com/2011/03/rye-saison-with-brett.html>

# ithaca water

m = InfusionMash()
m.ingredient('grain','german pilsener','12.75lb',color='2L')
m.ingredient('grain','rye malt','3.75lb',color='3.5L')
m.ingredient('misc','rice hulls','3oz')
m.ingredient('water','strike','6.0gal')
m.property('temp','150F')
m.property('t_mashtun','68F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s, duration='90min')
b.ingredient('hops','styrian celeia','2.5oz',time='60min',aa='4.5%AA') #,note="sub for styrian goldings")
b.ingredient('hops','styrian celeia','1.5oz',time='10min',aa='4.5%AA') #,note="sub for styrian goldings")
b.ingredient('misc','irish moss','1tsp',time='15min')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Belle Saison (Danstar)','1pack')
#f.property('OG','1.070sg')
#f.property('ABV','8%ABV')
f.property('atten','80%atten')
r.add(f)

r.solve()
print r


