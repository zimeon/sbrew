#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Saison"

# ithaca water

m = InfusionMash()
m.ingredient('grain','pilsener','8.5lb')
m.ingredient('grain','wheat','2.0lb')
m.ingredient('grain','munich','0.75lb')
m.ingredient('grain','chocolate','0.5lb')
m.ingredient('grain-no-ppg','black patent','0.25lb')
m.ingredient('water','strike','5.3gal')
m.property('temp','148F')
m.property('t_mashtun','60F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','7.5gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time=Quantity('90min')
b.ingredient('hops','amarillo','1.25oz',time=Quantity('60min'),aa=Quantity('10.3%AA'))
b.ingredient('hops','hallertau','0.50oz',time=Quantity('0min'),aa=Quantity('4.1%AA')) #no saaz left
b.ingredient('misc','irish moss','1tsp',time=Quantity('15min'))
b.ingredient('misc','gypsum','5g')
#b.ingredient('sucrose','table sugar','1lb',time=Quantity('5min')) #forgot!
b.property('boil_end_volume', '6.5gal')
b.solve()
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast','Wyeast 3711 French Saison','1cake') #from #78
f.property('FG','1.005sg')
r.add(f)

print r


