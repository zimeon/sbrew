import re

conversions = { 'oz'  : { 'lb' : 1.0/16.0 } ,
                'gal' : { 'pt' : 8 }
              }

class Quantity:
    """Base class for all quantities.

    All quantities have a value and a unit.
    """

    def __init__(self, value=None, unit=None):
        if (value is None):
            self.unit = unit
        elif (unit is None):
            # try to parse value and unit from string
            m = re.match('\s*([-+]?\d+(\.\d*)?)\s*(\w+)\s*$', value)
            if (m):
                self.value=float(m.group(1))
                self.unit=m.group(3)
            else:
                self.value = float(value)
                self.unit = unit
        else:
            self.value = float(value)
            self.unit = unit

    def __str__(self):
        if (self.value is None):
            return("QuantityNotDefiend")
        elif (self.unit is None):
            return(str(self.value) + " (dimensionless)")
        else:
            return(str(self.value) + " " + str(self.unit))

    def __repr__(self):
        if (self.value is None):
            return("QuantityNotDefined")
        elif (self.unit is None):
            return(str(self.value))
        else:
            return(str(self.value) + str(self.unit))

    def to(self,new_unit):
        """Get value of this quantity in a specific unit.

        Used conversions in conversions dictionary of dictionaries
        to look up conversion factors. At present not smart enough
        to find a chain between two units but that should be possible
        add.

        e.g. lbs = weight.to('lb')
             temp=Quantity('10C')
             f = temp.to('F')
        """
        if (self.unit==new_unit):
            return(self.value)
        elif (self.unit in conversions and
                new_unit in conversions[self.unit]):
            return(self.value*conversions[self.unit][new_unit])
        elif (new_unit in conversions and
                self.unit in conversions[new_unit]):
            #inverse
            return(self.value/conversions[new_unit][self.unit])
        else:
            raise LookupError('unknown conversion requested from ' + 
                              self.unit + ' to ' + new_unit)

    def convert_to(new_unit):
        """Convert internal value to the new unit

        Piggbybacks on the to() method but changes the internal
        representation. Returns self.
        """
        self.value = self.to(new_unit)
        self.unit = new_unit
        return(self)

    def __add__(self,other):
        """Add two quantities, return result in units of first.
        """
        sum=self.value+other.to(self.unit)
        return(Quantity(sum,self.unit))

    def __sub__(self,other):
        """Subtract one quantity from another, return result in units of first.
        """
        sum=self.value-other.to(self.unit)
        return(Quantity(sum,self.unit))

#    def set(self,str):
#        if (
