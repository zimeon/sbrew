"""Model Carbonation."""
from .recipe import Recipe, MissingParam
from .quantity import Quantity

from scipy.optimize import fsolve


class Carbonation(Recipe):
    """Carbonation is a simple recipe with no sub-steps.

    The three parameters are temperature (temp), pressure, and the volumes of CO2
    per volume of beer, represented as a dimensionless number. With any two, the
    other can be calculated.
    """

    DEFAULT_NAME = 'carbonation'

    def __init__(self, name=None, duration=None, **kwargs):
        """Initialize Carbonation process."""
        super(Carbonation, self).__init__(**kwargs)

    def import_forward(self):
        """Import properties from previous step."""
        self.import_property('ABV')
        self.import_property('FG')

    def solve(self):
        """Either work out carbonation from params, or vice versa."""
        if (self.has_properties('temp', 'pressure', 'vol')):
            # nothing to work out
            pass
        elif (self.has_properties('temp', 'pressure')):
            self.property('vol', vols_obtained(self.property('temp').quantity,
                                               self.property('pressure').quantity))
        elif (self.has_properties('temp', 'vol')):
            self.property('pressure', psi_required(self.property('temp').quantity,
                                                   self.property('vol').quantity))
        elif (self.has_properties('pressure', 'vol')):
            self.property('temp', temp_required(self.property('pressure').quantity,
                                                self.property('vol').quantity))
        else:
            raise MissingParam("Can't solve carbonation, have %s properties" % (self.properties.keys()))

    def end_state_str(self):
        """Human readbale string to describe final state."""
        s = ''
        if (self.has_properties('temp', 'pressure', 'vol')):
            s = "Carbonation: %s @ %s requires %s CO2" % (
                self.property('vol').quantity,
                self.property('temp').quantity,
                self.property('pressure').quantity)
        return(s)


# Functions

def psi_required_raw(t, v):
    """Pressure (psi) required for CO2 volumes (dimensionless) at given temparature (t in F).

    From:
    http://www.homebrewtalk.com/f128/formula-dissolved-co2-152427/

    -16.6999 - 0.0101059 * T + 0.00116512 * T ^2 +
    0.173354 * T * Vol +4.24267 * Vol - 0.0684226 * Vol ^2

    where T is degrees F and Vol is volumes of CO2 you want. but I
    do agree that that is just a best fit equation.

    This formula agrees with the value in the table on p184 of Papazian,
    The Home Brewer's Companion.
    """
    p = (-16.6999 - 0.0101059 * t + 0.00116512 * t * t +
         0.173354 * t * v + 4.24267 * v - 0.0684226 * v * v)
    return(p)


def psi_required(temp, vol):
    """Pressure required for CO2 volumes at given temparature.

    Wrapper arounf psi_required_raw(..) handling Quantity conversions
    """
    return(Quantity(psi_required_raw(temp.to('F'), vol.value), 'psi'))


def vols_obtained_raw(t, p):
    """CO2 volumes (dimensionless) resulting from given temp (F) and pressure (psi).

    Implemented using from scipy.optimize.fsolve(..) around psi_required_raw(..)
    """
    v_guess = 0.5
    v = fsolve(lambda v: p - psi_required_raw(t, v), v_guess)
    return(v)


def vols_obtained(temp, pressure):
    """CO2 volumes resulting from given temp and pressure.

    Wrapper around vols_required_raw(..) handling Quantity conversions
    """
    return(Quantity(vols_obtained_raw(temp.to('F'), pressure.to('psi')), ''))


def temp_required_raw(p, v):
    """Temperature required at given pressure (psi) to obtain the given volumes of CO2 (dimensionless).

    Implemented using from scipy.optimize.fsolve(..) around psi_required_raw(..)
    """
    t_guess = 45
    t = fsolve(lambda t: p - psi_required_raw(t, v), t_guess)
    return(t)


def temp_required(pressure, vol):
    """Temperature required to produce gievn CO2 volumes at given pressure.

    Wrapper around vols_required_raw(..) handling Quantity conversions
    """
    return(Quantity(temp_required_raw(pressure.to('psi'), vol.to('dimensionless')), 'F'))
