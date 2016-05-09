#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Simeon's Session Bitter (SSB)"

# ithaca water

m = InfusionMash()
m.ingredient('grain','Marris Otter (TF)','6.0lb',color='4L')
m.ingredient('grain','Cara Gold (Crisp)','8oz',color='6L')
m.ingredient('grain','Crystal 55 (Simpsons)','8oz',color='55L')
m.ingredient('grain','Dark Wheat (Wyermann)','8oz',color='10L')
m.ingredient('water','strike','4.25gal')
m.property('temp','154F')
m.property('t_mashtun','60F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','6.2gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
# boil
b.ingredient('hops','EKG','1.5oz',time='60min',aa='5.0%AA')
b.ingredient('hops','EKG','0.5oz',time='15min',aa='5.0%AA')
b.property('boil_end_volume', '5.6gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','WLP013','1vial')
f.ingredient('hops','Fuggles','1.0oz',aa='4.3%AA')
f.property('FG','1.010sg')
r.add(f)

r.solve()
print(r)


