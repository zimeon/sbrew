from quantity import Quantity

class Mass(Quantity):
    """Mass.

    """

    def to(self, unit):
        if (unit == self.unit):
            pass
        elif (self.unit == 'F' and unit == 'C'):
            self.value = self.value * 5.0 / 9.0
        elif (self.unit == 'C' and unit == 'F'):
            self.value = self.value * 9.0 / 5.0
        else:
            pass
