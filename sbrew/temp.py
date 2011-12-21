from quantity import Quantity

class Temp(Quantity):
    """Temperature.

    """

    def hhh(self):
        pass

    def to(self, unit):
        """Override simple conversions in Quantity

        """
        if (unit == self.unit):
            return(self.value)
        elif (self.unit == 'F' and unit == 'C'):
            return((self.value-32.0)*5.0/9.0)
        elif (self.unit == 'C' and unit == 'F'):
            return((self.value*9.0/5.0)+32.0)
        else:
            raise LookupExcpetion("unknown temperatre conversion")
