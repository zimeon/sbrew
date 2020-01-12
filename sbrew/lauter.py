"""Base model for Lauter process."""
from .recipe import Recipe
from .ingredient import Ingredient
from .quantity import Quantity


class Lauter(Recipe):
    """Lauter process: start with mash, extract wort.

    Input is a Mash object of some type. Import parameters:
      total_grain - (dry) mass of grain in mash
      total_water - volume of water in mash
      total_points - expected number of gravity points

    At the end of the lauter the key properties are

      wort_volume - volume of wort extracted
      wort_gravity - gravity of the wort extracted
    """

    DEFAULT_NAME = 'lauter'

    def __init__(self, **kwargs):
        """Initialize Lauter object."""
        super(Lauter, self).__init__(**kwargs)
        self.extra_info = None  # extra info for end_state_str

    def import_forward(self):
        """Import properties from previous step where available."""
        self.import_property('total_grain', 'grain')
        self.import_property('total_water', 'water')
        self.import_property('total_points', 'total_points')
        self.import_property('MCU')

    def import_backward(self):
        """Import properties from next step where available."""
        pass

    def solve(self):
        """Blank, exception."""
        raise Exception("Need to override Lauter solve()")

    def end_state_str(self):
        """Return string describing end state of step."""
        s = ''
        wv = self.property('wort_volume', default=None)
        if (wv is not None):
            s += str(wv.quantity) + ' wort'
        wg = self.property('wort_gravity', default=None)
        if (wg is not None):
            s += ' at ' + str(wg.quantity)
        if (self.extra_info is not None):
            s += ' (' + self.extra_info + ')'
        return(s)
