from quantity import Quantity
import re

class Property:
    """Representation of one property

    p1 = Property('temp','122F')
    p2 = Property('temp',123.2,'F')
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

    def short_str(self):
        """Short human readable string representation, exlcuding extra info"""
        s = ""
        if (self.name != 'time' and self.name != self.quantity.unit):
            s += self.name + " "
        s += str(self.quantity)
        return(s)

    def __str__(self):
        """Human readable string version of object

        Default form is "name     quantity"
        """
        s = "{0:15s}  {1:10s}".format(self.name,str(self.quantity))
        if (len(self.extra)>0):
            s += "  ( "
            for e in sorted(self.extra.keys()):
               s += "{0:6s}, ".format(self.extra[e])
            s += ")"
        return s
