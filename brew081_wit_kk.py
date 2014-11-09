#!/usr/bin/env python

from sbrew import *

r = Recipe("Wit for K&K")

m = StepMash()
m.ingredient(Ingredient('grain','pilsner ','5lb'))
m.ingredient(Ingredient('grain','wheat flakes','4lb'))
m.ingredient(Ingredient('grain','munich','8oz'))
m.add_step('infuse',volume='4.6gal',temp='122F')
m.add_step('rest',time='15min')
m.add_step('heat',temp='152F',time='30min')
m.add_step('rest',time='60min')
m.add_step('heat',temp='160F',time='5min')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','6.75gal')
r.add(s)

b = Boil(start=s,duration="90min")
b.property('boil_start_volume','6.75gal')
b.property('boil_end_volume','6.0gal')
b.ingredient(Ingredient('hops','hallertau','0.33oz',time='60min',aa='4.1%AA'))
b.ingredient(Ingredient('hops','hallertau','1.0oz',time='60min',aa='4.6%AA'))
r.add(b)

f = Ferment(start=b)
f.ingredient(Ingredient('yeast','Safbrew WB-06','1packet'))
r.add(f)

beer = Beer(start=f)
beer.property('bitterness','10IBU')
beer.property('abv','5.0%ABV')

r.solve()
print r


