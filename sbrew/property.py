"""Model for Property."""

from .quantity import Quantity
import re

class NoProperty(object):
    """Class used to represent 'no property' default."""

    def __str__(self):
        """Return human readable string."""
        return('NoProperty')


class MissingProperty(Exception):
    """Exception because of missing property."""

    def __init__(self, of=None, name=None, existing=None):
        """Initialize MissingPropery exception with optional context."""
        self.of = of
        self.name = name
        self.existing = existing

    def __str__(self):
        """Return human readable string with some context."""
        msg = "Missing property"
        if (self.name):
            msg += " %s" % (self.name)
        if (self.of):
            msg += " of %s" % (self.of)
        if (self.existing):
            msg += " (have %s)" % (self.existing)
        return(msg)


class Property:
    """Representation of one property.

    p1 = Property('temp','122F')
    p2 = Property('temp',123.2,'F')
    p3 = Property('temp',Quantity('124F'))
    p4 = Property('temp',Property('othertemp','125F')) #take Quantity from supplied Property
    p5 = Property('temp','126F',therm2='a',therm1='b')
    """

    def __init__(self, name, quantity, unit=None, **extra):
        """Initialize a Property."""
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
        """Return the value converted to unit.

        Shortcut to self.quantity.to(unit).
        """
        return self.quantity.to(unit)

    def short_str(self):
        """Short human readable string representation, excluding extra info.

        Avoid including the property name in cases where it will be obvious 
        from the units of the property.
        """
        s = ""
        if (self.name != 'time' and 
            self.name != 'aa' and
            self.name != self.quantity.unit):
            s += self.name + " "
        s += str(self.quantity)
        return(s)

    def __str__(self):
        """Human readable string version of Property.

        Default form is "name     quantity"
        """
        s = "{0:18s}  {1:10s}".format(self.name,str(self.quantity))
        if (len(self.extra)>0):
            extras = []
            for e in sorted(self.extra.keys()):
               extras.append("{0:6s}".format(self.extra[e]))
            s += "( " + ', '.join(extras) + ")"
        return s
