#!/usr/bin/env python

from sbrew import Quantity, Boil
from sbrew.refractometer import starting_gravity_to_brix

honey_sg = Quantity('1.36', 'sg')  # https://en.wikipedia.org/wiki/Honey
honey_ppg = 38  # Palmer "How to Brew" p245

apple_og = Quantity(input("Apple juice OG ? "))
honey_wt = Quantity(input("Honey weight ? "))
volume = Quantity(input("Total volume ? "))

print()
honey_vol = Quantity(honey_wt.to('lb') / (honey_sg.to('sg') * 8), 'gal')
print("Honey volume = ", str(honey_vol))
apple_vol = volume - honey_vol
print("Apple volume = ", str(apple_vol))

honey_pts = honey_wt.to('lb') * honey_ppg
print("Honey points = %.1f" % (honey_pts))
apple_pts = apple_vol.to('gal') * (apple_og.to('sg') - 1.0) * 1000
print("Apple points = %.1f" % (apple_pts))

og = Quantity(((honey_pts + apple_pts) / (volume.to('gal') * 1000.0) + 1.0), 'sg')
print()
print("OG = ", str(og))
print("OG = ", str(starting_gravity_to_brix(og)))
