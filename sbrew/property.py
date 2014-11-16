from quantity import Quantity
import re

class NoProperty(object):
    """Class used to represent 'no property' default"""
    def __str__(self):
        return('NoProperty')

class Property:
    """Representation of one property

    p1 = Property('temp','122F')
    p2 = Property('temp',123.2,'F')
    p3 = Property('temp',Quantity('124F'))
    p4 = Property('temp',Property('othertemp','125F')) #take Quantity from supplied Property
    p5 = Property('temp','126F',therm2='a',therm1='b')
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
        """Short human readable string representation, excluding extra info

        Avoid including the property name in cases where it will be obvious 
        from the units of the property.
        """
        s = ""
        if (self.name != 'time' and 
            self.name != 'AA' and
            self.name != self.quantity.unit):
            s += self.name + " "
        s += str(self.quantity)
        return(s)

    def __str__(self):
        """Human readable string version of object

        Default form is "name     quantity"
        """
        s = "{0:18s}  {1:10s}".format(self.name,str(self.quantity))
        if (len(self.extra)>0):
            extras = []
            for e in sorted(self.extra.keys()):
               extras.append("{0:6s}".format(self.extra[e]))
            s += "( " + ', '.join(extras) + ")"
        return s
