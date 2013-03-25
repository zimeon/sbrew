#!/usr/bin/env python

from sbrew.quantity import Quantity
from sbrew.carbonation import psi_required

t = Quantity(raw_input("Temperature ? "))
v = Quantity(raw_input("Volumes of CO2 required (float)? "))
p = psi_required(t,v)
print "%.1f @ %s requires %s" % (v.value,t,p)
