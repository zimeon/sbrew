from quantity import Quantity
import re

class Property:
    """Representation of one property

    p = Property('temp','122F')
    """

    def __init__(self, name, quantity, unit=None, **extra):
        self.name = name
        self.extra = {}
        self.extra.update(extra)
        if (isinstance(quantity, Quantity)):
            self.quantity = quantity
        if (isinstance(quantity, Property)):
            # discard name and just take quantity
            self.quantity = quantity.quantity
        else:
            self.quantity = Quantity(quantity, unit)

    def to(self,unit):
        """Shortcut to self.quantity.to(unit)"""
        return self.quantity.to(unit)

    def __str__(self):
        """Human readable string version of object

        Default form is "name     quantity"
        """
        s = "{0:15s}  {1:10s}".format(self.name,str(self.quantity))
        if (self.extra):
            for e in sorted(self.extra.keys()):
		s += "  ({0:6s})".format(self.extra[e])
        return s
