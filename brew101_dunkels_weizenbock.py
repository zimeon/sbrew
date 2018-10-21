#!/usr/bin/env python

from sbrew import *

r = Recipe("Dunkels Weizenbock")

m = DecoctionMash()
m.ingredient('grain', 'pale wheat malt', '6lb', color='2L')
m.ingredient('grain', 'dark/red wheat malt', '2lb', color='8L')
m.ingredient('grain', 'munich malt', '3lb', color='10L')
m.ingredient('grain', 'pilsener malt', '3lb', color='2L')
m.ingredient('grain', 'coffee malt', '8oz', color='165L')
m.ingredient('grain', 'chocolate malt', '3oz', color='375L')
m.ingredient('adjunct', 'rice hulls', '4oz')
# m.total_grains(Quantity('9.5lb'))
m.add_step('infuse', volume='4.25gal', temp='108F')
m.add_step('rest', time='5min')
m.add_step('heat', temp='122F', time='10min')
m.add_step('rest', time='15min')
d1 = m.split(time='5min', remove='40%')
d1.add_step('heat', temp='160F', time='15min')
d1.add_step('rest', time='15min')
d1.add_step('heat', temp='212F', time='15min')
d1.add_step('boil', time='20min')
m.mix(decoction=d1, time='10min')
m.add_step('adjust', temp='147F')
m.add_step('rest', time='20min')
m.add_step('heat', temp='160F', time='7min')
m.add_step('rest', time='13min')
m.add_step('infuse', temp='170F', infusion_temp='212F',
           volume='1.2gal', time='5min')
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
r.add(s)

b = Boil(start=s, duration="90min")
b.ingredient('hops', 'uk ekg', '1.5oz', time='60min', aa='6.5%AA')
b.ingredient('hops', 'hallertau', '0.5oz', time='15min', aa='2.7%AA')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'wyeast 3056 bavarian weizen', '1yeast_cake')
f.property('atten', '80.0%atten')
r.add(f)

r.solve()
print r
