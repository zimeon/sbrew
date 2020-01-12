#!/usr/bin/env python

from sbrew import *

r = Recipe()
r.name = "Robust Porter"

# Ithaca water

m = InfusionMash()
m.ingredient('grain', 'marris otter', '11.0lb', color='4L')
m.ingredient('grain', 'chocolate (Weyermann Carafa I)', '1lb', color='350L')
m.ingredient('grain', 'simpsons coffee', '2oz', color='150L')
m.ingredient('grain', 'crystal 55', '8oz', color='55L')
m.ingredient('grain', 'debittered black', '4oz', color='500L')
m.ingredient('water', 'strike', '5.7gal')
m.property('temp', '150F')
m.property('t_mashtun', '65F')
m.solve()
r.add(m)

s = BatchSparge(start=m)
s.property('wort_volume', '7.0gal')
s.solve()
r.add(s)

b = Boil(start=s)
b.time = Quantity('60min')
b.ingredient('hops', 'centennial', '0.25oz', time=Quantity('60min'), aa=Quantity('10.4%AA'))
b.ingredient('hops', 'us perle', '1.0oz', time=Quantity('60min'), aa=Quantity('5.3%AA'))
b.ingredient('hops', 'willamette', '1.0oz', time=Quantity('60min'), aa=Quantity('4.6%AA'))
b.ingredient('hops', 'Cascade (whole)', '1.5oz', time=Quantity('15min'), aa=Quantity('4%AA'))
b.ingredient('misc', 'irish moss', '1tsp', time=Quantity('15min'))
b.property('boil_end_volume', '6.5gal')
r.add(b)

f = Ferment(start=b)
f.ingredient('yeast', 'safale us-05', '1pack')
f.property('FG', '1.016sg')
r.add(f)

r.solve()
print(r)
