#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Wheat Rauchbier (Barrel Brew)"

# ithaca water

m = DecoctionMash()
m.ingredient('grain','smoked wheat malt','8lb',color='9L')
m.ingredient('grain','munich','1.25lb',color='20L')
m.ingredient('grain','pilsner 2-row german','1.2lb',color='2L')
m.ingredient('grain','caravienne','13oz',color='22L')
m.ingredient('grain','carafa II','1.8oz',color='412L')
# mash
m.add_step('infuse',volume='4.0gal',temp='126F')
m.add_step('heat',temp='122F',time='10min')
m.add_step('rest',time='15min')
d1=m.split(time='5min',remove='40%')
d1.add_step('heat',temp='160F',time='15min')
d1.add_step('rest',time='15min')
d1.add_step('heat',temp='212F',time='15min')
d1.add_step('boil',time='20min')
m.mix(decoction=d1,time='10min')
m.add_step('adjust',temp='154F')
m.add_step('rest',time='20min')
m.add_step('heat',temp='165F',time='7min')
m.add_step('rest',time='13min')
m.add_step('infuse',temp='168F',infusion_temp='212F',volume='1.25gal',time='5min')
m.property('temp','150F')
m.property('t_mashtun','68F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('90min')
b.ingredient('hops','tettnang','1.6oz',time='60min',aa='4.5%AA')
b.ingredient('hops','tettnang','0.25oz',time='5min',aa='4.5%AA')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Wyeast Octoberfest Lager #2633','1starter')
#f.property('ABV','8%ABV')
f.property('atten','75%atten')
r.add(f)

r.solve()
print(r)


