#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Cascade Special Bitter"

# ithaca water, plus
# 15g gypsum in 12gal strike water
#w = Water()
#w.ingredient('gypsum','','12g')

m = InfusionMash()
m.ingredient('grain','2-row','9.0lb',color='4L')
m.ingredient('grain','Caravienne','0.5lb',color='21L')
m.ingredient('grain','Coffee 150','0.25lb',color='150L')
m.ingredient('water','strike','5.25gal')
m.property('temp','150F')
m.property('t_mashtun','59F')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
b.ingredient('hops','Centennial','1.0oz',time='60min',aa='8.5%AA')
b.ingredient('hops','US Perle','0.2oz',time='60min',aa='5.3%AA')
b.ingredient('hops','Cascade (whole)','1.0oz',time='15min',aa='4%AA')
b.ingredient('hops','Cascade (whole)','1.0oz',time='0min',aa='4%AA')
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Wyeast London Ale III 1318','1pack')
f.property('atten','73%atten')
r.add(f)

r.solve()
print(r)
