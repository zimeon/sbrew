#!/usr/bin/env python

from sbrew import *

g = Quantity(raw_input("Gravity (e.g. 1.040SG)? "))
v = Quantity(raw_input("Volumes (e.g. 4qt)? "))
# 42ppg for DME
lb = (g.to('SG')-1.0) * 1000.0 * v.to('gal') / 42.0
m = Quantity(lb,"lb")
m.convert_to('oz')
print "%s @ %s requires %s DME" % (v,g,m)
