from quantity import Quantity
import re

class Ingredient:
    """Representation of one ingredient

    i = Ingredient('grain','belgian pilsner','9.75lb')
    i = Ingredient('grain','belgian pilsner',9.75,'lb')
    """

    def __init__(self, type, name, quantity, unit=None, **extra):
        self.type = type
        self.name = name
        self.pct = None
        self.extra = {}
        self.extra.update(extra)
        if (isinstance(quantity, Quantity)):
            self.quantity = quantity
        else:
            self.quantity = Quantity(quantity, unit)

    def __str__(self):
        """Human readable string version of object

        Default form is "type name quantity" but also will append information
        from some extra parameters: pct,
        """
        s = "{0:10s}  {1:30s}   {2:10s}".format(self.type,self.name,str(self.quantity))
	if (self.pct):
	    s += "   ({0:5.1f}%)".format(self.pct)
        if (self.extra):
            for e in sorted(self.extra.keys()):
		s += "  ({0:6s})".format(self.extra[e])
        return s
