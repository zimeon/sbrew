#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Brew60 Loganberry Stout"

m = InfusionMash()
m.subname = 'first infusion'
m.ingredient(Ingredient('grain','marris otter','7lb'))
m.ingredient(Ingredient('grain','roasted barley','14oz'))
m.ingredient(Ingredient('grain','flaked barley','2lb'))
m.ingredient('water','strike','2.5gal')
m.property('temp','122F')
m.property('t_mashtun','70F')
m.solve()
r.add(m)

m2 = InfusionMash(start=m)
m2.subname = 'second infusion'
m2.ingredient('water','strike','2.5gal')
m2.property('temp','152F')
m2.solve()
r.add(m2)

s = BatchSparge(start=m2)
s.property('boil_start_volume','6.5gal')
s.solve()
r.add(s)

b = Boil(duration='60min', start=s)
b.ingredient(Ingredient('hops','hallertau','3oz',time='60min',AA='4.3%AA'))
b.ingredient(Ingredient('hops','saaz','1oz',time='15min',AA='3.9%AA'))
b.ingredient(Ingredient('misc','irish moss','1tsp',time='15min'))
b.ingredient(Ingredient('sugar','cane sugar','1.1lb',time='15min'))
b.solve()
r.add(b)

f = Ferment(start=b)
f.subname = "ferment"
f.ingredient(Ingredient('yeast','white labs WLP550 Belgian Ale','1vial'))
f.property('temp','68F')
f.property('FG','1.012sg')
r.add(f)

c = Carbonation(start=f)
c.property('temp','68F')
c.property('vol','3volumes')
c.solve()
r.add(c)

print r.__str__(line_numbers=True)
