#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Brew58 Tarragon Belgian"

m = InfusionMash()
m.ingredient(Ingredient('grain','pilsner','9.25lb'))
m.ingredient(Ingredient('grain','caravienne belgian','1.25lb'))
m.ingredient(Ingredient('water','','3.98gal'))
mass_grain=m.total_grains()
shc_grain =Quantity("0.3822Btu/lb/F")
hc_grain=Quantity(mass_grain.to('lb')*shc_grain.to('Btu/lb/F'),'Btu/F')
shc_water=Quantity("1Btu/lb/F")
volume_water=m.total_water()
mass_water=Quantity(volume_water.to('pt'),'lb') #1lb == 1pt
hc_water=Quantity(mass_water.to('lb')*shc_water.to('Btu/lb/F'),'Btu/F')
shc_stainless=Quantity("0.120Btu/lb/F")
mass_mashtun=Quantity("9.5lb")
hc_mashtun=Quantity(mass_mashtun.to('lb')*shc_stainless.to('Btu/lb/F'),'Btu/F')
hc_rest=hc_grain+hc_mashtun
m.property('temp','150F')
m.property('t_mashtun','70F')
t_strike=Quantity( (((hc_water+hc_rest).value*150 - hc_rest.value*70) / hc_water.value), 'F')
print "V_strike     = " + str(volume_water)
print "T_strike     = " + str(t_strike)
print m

r.add(m)
print "Total grains = " + str(m.total_grains())

s = BatchSparge(mash=m)
s.property('v_boil','6.5gal')
s.solve()
r.add(s)

b = Recipe()
b.subname = "boil"
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
