#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="American West Coast IPA (Imperialish)"

# ithaca water

m = InfusionMash()
m.ingredient('grain','2 row','12.75lb',color='2L')
m.ingredient('grain','Biscuit','12oz',color='20L')
m.ingredient('water','strike','5.4gal')
m.property('temp','150F')
m.property('t_mashtun','60F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
# boil
b.ingredient('hops','Columbus','2.0oz',time='60min',aa='15.2%AA')
b.ingredient('hops','Centennial','2.0oz',time='60min',aa='9.0%AA')
b.ingredient('hops','Simcoe','1.0oz',time='60min',aa='12.3%AA')
# mid
b.ingredient('hops','Columbus','1.0oz',time='30min',aa='15.2%AA')
b.ingredient('hops','Simcoe','1.0oz',time='15min',aa='12.3%AA')
b.ingredient('sucrose','table sugar','1lb',time=Quantity('5min'))
# flame out
b.ingredient('hops','Centennial','1.0oz',time='0min',aa='9.0%AA')
b.ingredient('hops','Simcoe','1.0oz',time='0min',aa='12.3%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Safbrew S-05','1pack/starter')
# dry hop
f.ingredient('hops','Centennial','1.0oz',aa='8.7%AA')
f.ingredient('hops','Simcoe','1.0oz',aa='12.3%AA')
f.property('atten','80%atten')
r.add(f)

r.solve()
print r


