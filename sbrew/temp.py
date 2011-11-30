from quantity import Quantity

class Temp(Quantity):
    """Temperature.

    """

    def hhh(self):
        pass

    def to(self, unit):
        if (unit == self.unit):
            pass
        elif (self.unit == 'F' and unit == 'C'):
            self.value=(self.value-32.0)*5.0/9.0
            self.unit='C'
        elif (self.unit == 'C' and unit == 'F'):
            self.value=(self.value*9.0/5.0)+32.0
            self.unit='F'
        else:
            pass
        return(self)
