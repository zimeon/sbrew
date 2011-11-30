import re

class Quantity:
    """Base class for all quantities.

    All quantities have a value and a unit.
    """

    def __init__(self, value=None, unit=None):
        self.value = value
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

#    def set(self,str):
#        if (
