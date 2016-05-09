#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Logan Farm"

# ithaca water

m = InfusionMash()
m.ingredient('grain','pilsener','8.5lb')
m.ingredient('grain','wheat','3.5lb')
m.ingredient('grain','munich','0.75lb')
m.ingredient('water','strike','5.0gal')
m.property('temp','148F')
m.property('t_mashtun','60F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.50gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time=Quantity('90min')
b.ingredient('hops','amarillo','0.4oz',time=Quantity('60min'),aa=Quantity('8.2%AA'))
b.ingredient('hops','willamette','0.50oz',time=Quantity('60min'),aa=Quantity('5.2%AA'))
b.ingredient('hops','ekg','0.50oz',time=Quantity('60min'),aa=Quantity('6.4%AA'))
b.ingredient('hops','saaz','0.50oz',time=Quantity('0min'),aa=Quantity('3.2%AA'))
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.ingredient('misc','gypsum','5g')
# would have been 1lb, but had only 5oz
b.ingredient('sucrose','table sugar','5oz',time=Quantity('5min'))
b.ingredient('fruit','loganberry mush/juice)','3lb',
             time=Quantity('0min'),extract=Quantity('15%'))  # no idea about extract 
b.property('boil_end_volume', '6.5gal')
b.solve()
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','White Labs WLP670 American Farmhouse Ale','1vial')
r.add(f)

print(r)


