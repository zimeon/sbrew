#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name="Warner Weisse"
m = DecoctionMash()
m.ingredient(Ingredient('grain','marris otter (tf)','63%'))
m.ingredient(Ingredient('grain','wheat malt (tf)','37%'))
m.add_step('infuse',volume='3.6gal',temp='106F')
m.add_step('heat',temp='122F',time='10min')
m.add_step('rest',time='15min')
d1=m.add_step('split',time='5min',remove='40%')
d1.add_step('heat',temp='160F',time='15min')
d1.add_step('rest',time='15min')
d1.add_step('heat',temp='212F',time='15min')
d1.add_step('boil',time='20min')
m.add_step('mix',time='10min',portion=d1)
m.add_step('adjust',temp='147F')
m.add_step('rest',time='20min')
m.add_step('heat',temp='160F',time='7min')
m.add_step('rest',time='13min')
m.add_step('infuse',temp='170F',infusion_tem='212F',volume='1.2gal',time='5min')
r.add(m)

s = Lauter()
r.add(s)

b = Recipe()
b.subname = "boil"
b.ingredient(Ingredient('hops','hallertau','1oz',time='60min',aa='4.3%'))
b.ingredient(Ingredient('hops','hallertau','0.25oz',time='15min',aa='4.3%'))
r.add(b)

f = Recipe()
f.subname = "ferment"
f.ingredient(Ingredient('yeast','wyeast 3056 bavarian weizen','1packet'))
r.add(f)

print r


mass_grain=m.total_grains(Quantity("9.5lb"))
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


print r


