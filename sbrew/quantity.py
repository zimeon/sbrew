class Quantity:
    """Base class for all quantities.

    All quantities have a value and a unit.
    """

    def __init__(self):
        self.value = None
        self.unit = None

#    def __init__(self,value,unit):
#        self.value = value
#        self.unit = unit

    def str(self):
        if (self.value is None):
            return("None")
        elif (self.unit is None):
            return(str(self.value) + " (dimensionless)")
        else:
            return(str(self.value) + " " + str(self.unit))
