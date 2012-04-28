#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="TestBier"

m = Mash()
m.ingredient(Ingredient('grain','marris otter','7.0lb'))
m.ingredient(Ingredient('grain','crystal 55','0.5lb'))
m.ingredient(Ingredient('grain','brown malt','1.0lb'))
m.ingredient(Ingredient('grain','british chocolate (simpsons)','0.5lb'))
mass_grain=m.total_grains()
shc_grain =Quantity("0.3822Btu/lb/F")
hc_grain=Quantity(mass_grain.to('lb')*shc_grain.to('Btu/lb/F'),'Btu/F')
shc_water=Quantity("1Btu/lb/F")
volume_water=Quantity("4.74gal")
mass_water=Quantity(volume_water.to('pt'),'lb') #1lb == 1pt
hc_water=Quantity(mass_water.to('lb')*shc_water.to('Btu/lb/F'),'Btu/F')
shc_stainless=Quantity("0.120Btu/lb/F")
mass_mashtun=Quantity("10lb")
hc_mashtun=Quantity(mass_mashtun.to('lb')*shc_stainless.to('Btu/lb/F'),'Btu/F')
hc_rest=hc_grain+hc_mashtun
t_strike=Quantity( (((hc_water+hc_rest).value*152 - hc_rest.value*64) / hc_water.value), 'F')
print "Total grains = " + str(mass_grain)
print "V_strike     = " + str(volume_water)
print "T_strike     = " + str(t_strike)
m.ingredient(Ingredient('water','',volume_water,temp=t_strike))
r.add(m)

s = BatchSparge()
s.wort_volume=Quantity('6.5gal')
r.add(s)

b = Recipe()
b.subname = "boil"
b.time=Quantity('60min')
b.ingredient(Ingredient('hops','stryian goldings','1oz',time=Quantity('60min')))
b.ingredient(Ingredient('hops','stryian goldings','1oz',time=Quantity('15min')))
b.ingredient(Ingredient('misc','irish moss','1tsp',time=Quantity('15min')))
r.add(b)

f = Recipe()
f.subname = "ferment"
f.ingredient(Ingredient('yeast','white labs WLP550 belgian ale','1vial'))
f.ingredient(Ingredient('hops','stryian goldings','2oz'))
r.add(f)

print r


