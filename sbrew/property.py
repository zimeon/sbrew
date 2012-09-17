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
        else:
            self.quantity = Quantity(quantity, unit)

    def __str__(self):
        """Human readable string version of object

        Default form is "name     quantity"
        """
        s = "{0:10s}  {1:10s}".format(self.name,str(self.quantity))
        if (self.extra):
            for e in sorted(self.extra.keys()):
		s += "  ({0:6s})".format(self.extra[e])
        return s
