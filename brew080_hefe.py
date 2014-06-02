#!/usr/bin/env python

from sbrew import *

r = Recipe("Warner Weisse")

m = DecoctionMash()
m.ingredient(Ingredient('grain','marris otter (tf)','37%'))
m.ingredient(Ingredient('grain','wheat malt (tf)','63%'))
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
m.add_step('infuse',temp='170F',infusion_temp='212F',volume='1.2gal',time='5min')
m.total_grains(Quantity('9.5lb'))
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume','6.5gal')
s.solve()
r.add(s)

b = Boil(start=s,duration="60min")
b.ingredient(Ingredient('hops','hallertau','1oz',time='60min',aa='4.3%AA'))
b.ingredient(Ingredient('hops','hallertau','0.25oz',time='15min',aa='4.3%AA'))
b.property('boil_end_volume','6.0gal')
r.add(b)

f = Ferment(start=b)
f.ingredient(Ingredient('yeast','wyeast 3056 bavarian weizen','1packet'))
r.add(f)

#beer = Beer(start=f)
#beer.property('bitterness','10IBU')
#beer.property('abv','5.0%ABV')

r.solve()
print r


