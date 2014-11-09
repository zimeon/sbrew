from quantity import Quantity
from property import Property
import re

class Ingredient:
    """Representation of one ingredient

    i = Ingredient('grain','belgian pilsner','9.75lb')
    i = Ingredient('grain','belgian pilsner',9.75,'lb')
    """

    def __init__(self, type, name, quantity, unit=None, *properties, **properties_kv):
        self.type = type
        self.name = name
        self.pct = None
        self.properties = {}
        for p in properties:
            self.properties[p.name] = p
        for k in properties_kv.keys():
            p = Property(k,properties_kv[k])
            self.properties[k] = p
        if (isinstance(quantity, Quantity)):
            self.quantity = quantity
        else:
            self.quantity = Quantity(quantity, unit)

    def __str__(self):
        """Human readable string version of object

        Default form is "type name quantity" but also will append information
        from pct and properties
        """
        s = "{0:15s}  {1:30s}   {2:10s}".format(self.type,self.name,str(self.quantity))
        if (self.pct):
            s += "   ({0:5.1f}%)".format(self.pct)
        if (len(self.properties)>0):
            prop_strs = []
            for e in sorted(self.properties.keys()):
                prop_strs.append(self.properties[e].short_str())
            s += "  (" + ", ".join(prop_strs) + ")"
        return s
