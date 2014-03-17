#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Saison"

# ithaca water

m = InfusionMash()
m.ingredient('grain','pilsener','6.0lb')
m.ingredient('grain','wheat','3.0lb')
m.ingredient('grain','munich','0.75lb')
m.ingredient('water','strike','4.9gal')
m.property('temp','148F')
m.property('t_mashtun','60F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.0gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time=Quantity('60min')
b.ingredient('hops','amarillo','0.75oz',time=Quantity('60min'),aa=Quantity('10.0%AA'))
b.ingredient('hops','amarillo','0.25oz',time=Quantity('15min'),aa=Quantity('10.0%AA'))
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.ingredient('sucrose','table sugar','1lb',time=Quantity('1min'))
b.property('boil_end_volume', '6.5gal')
b.solve()
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','us-05','1packet')
r.add(f)

print r


