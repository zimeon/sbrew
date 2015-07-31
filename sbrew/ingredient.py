from quantity import Quantity
from property import Property, NoProperty, MissingProperty
import re

class Ingredient:
    """Representation of one ingredient

      i = Ingredient('grain','belgian pilsner','9.75lb')
      i = Ingredient('grain','belgian pilsner',9.75,'lb')

    or alternatively, the fraction of this ingredient may be set:

      i = Ingredient('grain','belgian pilsner',pct=80.0)

    and additionally, properties may be added as named parameters:

      i = Ingredient('grain','belgian pilsner',pct=80.0,temp=Quantity("65F"))
    """

    def __init__(self, type, name, quantity=None, unit=None, pct=None, **properties_kv):
        self.type = type
        self.name = name
        self.pct = pct
        self.properties = {}
        self.quantity = None
        for k in properties_kv.keys():
            p = Property(k,properties_kv[k])
            self.properties[k] = p
        if (isinstance(quantity, Quantity)):
            self.quantity = quantity
        elif (quantity is not None):
            self.quantity = Quantity(quantity, unit)

    def property(self,p,quantity=None,unit=None,default=NoProperty):
        """Add/get property to this ingredient

        This is getter and setter for the property p. Perhaps not
        properly pythonic but p=Property and quantity!=None implies set,
        otherwise get.

        Returns None or the value of default is there is no such property.
        If default is not set then a MissingProperty exception is raised.
        """
        if (not isinstance(p,Property)):
            if (quantity is None):
                q = self.properties.get(p)
                if (q is None):
                    if (default == NoProperty):
                        raise MissingProperty(self.name,p,self.properties.keys())
                    elif (default is None):
                        # request it to return None in this case that property does not exist
                        return None
                    else:
                        # get quantity of this property (else None)
                        return(Property(p,default))
                return(q)
            else:
                # set with values given
                name = p
                p = Property(name,quantity,unit)
        else:
            name = p.name
        self.properties[name]=p
        return(p)

    def has_properties(self,*args):
        """True if recipe has the properties listed, else false"""
        for property in args:
            if (property not in self.properties):
                return(False)
        return(True)

    def has_property(self,*arg):
        """Another name for has_properties()"""
        return(self.has_properties(*arg))        

    def __str__(self):
        """Human readable string version of object

        Default form is "type name quantity" but also will append information
        from pct and properties
        """
        s = "{0:15s}  {1:30s}".format(self.type,self.name)
        if (self.quantity):
            s += "   {0:10s}".format(str(self.quantity))
        if (self.pct):
            s += "   ({0:5.1f}%)".format(self.pct)
        if (len(self.properties)>0):
            prop_strs = []
            for e in sorted(self.properties.keys()):
                prop_strs.append(self.properties[e].short_str())
            s += "  (" + ", ".join(prop_strs) + ")"
        return s
