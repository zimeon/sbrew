#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Simeon's Session Bitter (SSB)"

# ithaca water

m = InfusionMash()
m.ingredient('grain','Marris Otter (TF)','7.5lb',color='4L')
m.ingredient('grain','Crystal 55 (Simpsons)','12oz',color='55L')
m.ingredient('grain','Crystal 120 (Briess)','4oz',color='120L')
m.ingredient('grain','Red Wheat','8oz',color='10L')
m.ingredient('water','strike','4.5gal')
m.property('temp','154F')
m.property('t_mashtun','60F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
# boil
b.ingredient('hops','Fuggles','1.75oz',time='60min',aa='5.3%AA')
b.ingredient('hops','Fuggles','0.5oz',time='15min',aa='5.3%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Wyeast1028 (==WLP013) London Ale','1pack')
f.ingredient('hops','Fuggles','1.0oz',aa='5.3%AA')
f.property('FG','1.010sg')
r.add(f)

r.solve()
print r


