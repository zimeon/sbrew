from quantity import Quantity

class Ingredient:
    """Representation of one ingredient

    i = Ingredient('grain','belgian pilsner','9.75lb')
    """

    def __init__(self, type, name, quantity, unit=None):
        self.type = type
        self.name = name
        if (isinstance(quantity, Quantity)):
            self.quantity = quantity
        else:
            self.quantity = Quantity(quantity, unit)

    def __str__(self):
        return "{0:10s}  {1:30s}   {2:20s}".\
               format(self.type,self.name,str(self.quantity))

