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
print m

m2 = InfusionMash(start=m)
m2.subname = 'second infusion'
m2.ingredient('water','strike','2.5gal')
m2.property('temp','152F')
m2.solve()
r.add(m2)

s = BatchSparge()
r.add(s)

b = Boil(duration='60min')
b.ingredient(Ingredient('hops','hallertau','3oz'))
b.ingredient(Ingredient('hops','saaz','1oz'))
b.ingredient(Ingredient('misc','irish moss','1tsp'))
b.ingredient(Ingredient('misc','tarragon(fresh)','120g'))
b.ingredient(Ingredient('sugar','cane sugar','1.1lb'))
r.add(b)


f = Recipe()
f.subname = "ferment"
f.ingredient(Ingredient('yeast','white labs WLP550 Belgian Ale','1vial'))
r.add(f)

print r

carb_temp=Quantity('68F')
carb_vols=Quantity('3volumes')
psi = psi_required(carb_temp,carb_vols)
print "Carbonation: %s @ %s requires %s CO2" % (carb_vols,carb_temp,psi)
