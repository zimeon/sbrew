#!/usr/bin/env python

from sbrew import *

r = Recipe("Warner Weisse")

m = DecoctionMash()
m.ingredient('grain', 'marris otter (tf)', '40%')
m.ingredient('grain', 'wheat malt (tf)', '60%')
m.total_grains(Quantity('10.0lb'))
m.add_step('infuse', volume='3.6gal', temp='108F')
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
s.property('wort_volume', '6.75gal')
r.add(s)

b = Boil(start=s, duration="60min")
# b.ingredient('hops', 'hallertau', '12IBU', time='60min', aa='2.7%AA')
b.ingredient('hops', 'hallertau', '0.75oz', time='60min', aa='2.7%AA')
b.ingredient('hops', 'hallertau', '0.65oz', time='60min', aa='3.7%AA')
b.ingredient('hops', 'hallertau', '0.25oz', time='15min', aa='2.7%AA')
b.property('boil_end_volume', '6.25gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'wyeast 3056 bavarian weizen', '1packet')
f.property('atten', '80.0%atten')
r.add(f)

r.solve()
print(r)
