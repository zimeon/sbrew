#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Belgian Golden Barrel Sour Collab"

# ithaca water

m = InfusionMash()
m.ingredient('grain','Pilsener','9.7lb',color='2L')
m.ingredient('grain','Munich','1.0lb',color='10L')
m.ingredient('grain','Vienna','1.0lb',color='4L')
m.ingredient('grain','Crystal 55','8oz',color='55L')
m.ingredient('water','strike','5.2gal')
m.property('temp','151F')
m.property('t_mashtun','61F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('90min')
b.ingredient('hops','Hallertau','1.5oz',time='60min',aa='4.0%AA')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Wyeast Belgian Ardennes 3522','1pack/starter')
#f.property('ABV','8%ABV')
f.property('atten','73%atten')
f.property('temp','66F')
r.add(f)

r.solve()
print r


