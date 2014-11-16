from recipe import Recipe
from quantity import Quantity

EXTRACTS = { 'corn_sugar' : 42.0,
             'cane_sugar' : 46.0,
             'ldme': 36.0,
             'sucrose': 46.0  }

class WortAdditions(Recipe):
    """Non-mashed additions to a wort

    Additions may either by of the types listed in the EXTRACTS dictionary, which
    each have a ppg value specified, or else may have an explicit ppg value 
    given.
    """

    DEFAULT_NAME='wort additions'

    def __init__(self, **kwargs):
        super(WortAdditions, self).__init__(**kwargs)        

    def import_forward(self):
        self.import_property('wort_volume')
        self.import_property('wort_gravity', 'start_gravity')
        self.import_property('MCU')

    def solve(self):
        """Calculate the bitterness and the volume at end of boil

        FIXME - currently can only solve forward

        FIXME - should cater for possible MCU additions
        """
        wort_gravity = self.property('start_gravity').to('sg') +\
                       ( self.total_points().to('points') / self.property('wort_volume').to('gal') / 1000.0 )
        self.property('wort_gravity', Quantity(wort_gravity,'sg') )

    def total_points(self):
        """Calculate total points of the wort additions"""
        total_points = 0.0
        for ingredient in self.ingredients:
            if (ingredient.has_property('ppg')):
                # Use given value if specified
                total_points += ingredient.property('ppg').to('ppg') * ingredient.quantity.to('lb')
            else:
                total_points += EXTRACTS[ingredient.type] * ingredient.quantity.to('lb')
        return( Quantity(total_points,'points') )

