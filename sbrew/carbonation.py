from recipe import Recipe
from quantity import Quantity

class Carbonation(Recipe):
    """The act of carbonating is a simple recipe with no sub-steps.
    """

    DEFAULT_NAME='carbonation'

    def __init__(self, name=None, duration=None, **kwargs):
        super(Carbonation, self).__init__(**kwargs)        

    def import_forward(self):
        self.import_property('ABV')
        self.import_property('FG')

    def solve(self):
        """Either work out carbonation from params, or vice versa
        """
        if (self.has_properties('temp','pressure','vol')):
            # nothing to work out
            pass
        elif (self.has_properties('temp','pressure')):
            self.property( 'pressure', vols_c02(self.property('temp').quantity,
                                                self.property('pressure').quantity) )
        elif (self.has_properties('temp','vol')):
            self.property( 'pressure', psi_required(self.property('temp').quantity,
                                                    self.property('vol').quantity) )

    def end_state_str(self):
        s = ''
        if (self.has_properties('temp','pressure','vol')):
            s = "Carbonation: %s @ %s requires %s CO2\n" % (
                self.property('vol').quantity,
                self.property('temp').quantity,
                self.property('pressure').quantity)
        return(s)


##### Functions #####

def psi_required(temp, vol):
    """Pressure required for CO2 volumes at given temparature.
    
    From:
    http://www.homebrewtalk.com/f128/formula-dissolved-co2-152427/
    
    -16.6999 - 0.0101059 * T + 0.00116512 * T ^2 + 
    0.173354 * T * Vol +4.24267 * Vol - 0.0684226 * Vol ^2
    
    where T is degrees F and Vol is volumes of CO2 you want. but I 
    do agree that that is just a best fit equation.
    
    This formula agrees with the value in the table on p184 of Papazian,
    The Home Brewer's Companion.
    """
    t=temp.to('F')
    v=vol.value
    p=(-16.6999 - 0.0101059*t + 0.00116512*t*t + \
            0.173354*t*v + 4.24267*v - 0.0684226*v*v)
    return(Quantity(p,'psi'))

def vols_obtained(temp, pressure):
    """CO2 volumes resulting from given temp and pressure
    """
    raise Exception("Not yet implemented vols_obtained")    
