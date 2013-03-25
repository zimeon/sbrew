#!/usr/bin/env python
from sbrew import *

r = Recipe()
r.name="Complete Breakfast Brew#56"

m1 = InfusionMash()
m1.subname = 'oatmeal pre-mash'
m1.ingredient(Ingredient('grain','oatmeal','1.5lb'))
m1.ingredient(Ingredient('water','','1.1gal'))
m1.property('temp','122F')
m1.property('duration','30min')
print m1

m = InfusionMash(start=m1)
m.subname = 'main mash'
m.ingredient(Ingredient('grain','marris otter','8.0lb'))
m.ingredient(Ingredient('grain','crystal 55','1.0lb'))
m.ingredient(Ingredient('grain','british chocolate (simpsons)','0.75lb'))
m.ingredient(Ingredient('grain','roast','0.25lb'))
m.ingredient(Ingredient('water','strike','3.98gal'))
m.property('temp','152F')
m.property('duration','60min')
mass_grain=m.total_grains()
shc_grain =Quantity("0.3822Btu/lb/F")
hc_grain=Quantity(mass_grain.to('lb')*shc_grain.to('Btu/lb/F'),'Btu/F')
shc_water=Quantity("1Btu/lb/F")
volume_water=m.total_water()
mass_water=Quantity(volume_water.to('pt'),'lb') #1lb == 1pt
hc_water=Quantity(mass_water.to('lb')*shc_water.to('Btu/lb/F'),'Btu/F')
shc_stainless=Quantity("0.120Btu/lb/F")
mass_mashtun=Quantity("10lb")
hc_mashtun=Quantity(mass_mashtun.to('lb')*shc_stainless.to('Btu/lb/F'),'Btu/F')
hc_rest=hc_grain+hc_mashtun
t_strike=Quantity( (((hc_water+hc_rest).value*152 - hc_rest.value*64) / hc_water.value), 'F')
print "V_strike     = " + str(volume_water)
print "T_strike     = " + str(t_strike)
print m

r.add(m)
m.add_mash(m1)
print "Total grains = " + str(m.total_grains())

s = Recipe(start=m1)
s.subname = "sparge"
r.add(s)

b = Recipe(start=s)
b.subname = "boil"
b.property('v_boil','6.5gal')
b.ingredient(Ingredient('hops','stryian goldings','1oz'))
b.ingredient(Ingredient('hops','stryian goldings','1oz'))
b.ingredient(Ingredient('misc','irish moss','1tsp'))
r.add(b)

f = Recipe()
f.subname = "ferment"
f.ingredient(Ingredient('yeast','white labs WLP013 London Ale','1cake'))
r.add(f)

c = Recipe()
c.subname = "post-fermentation addition"
c.ingredient(Ingredient('coffee','Gimme leftist espresso','800ml'))
r.add(c)

print r


