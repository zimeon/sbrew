from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from property import Property

class Boil(Recipe):
    """A boil is a simple recipe with no sub-steps.

    b = Boil(start=sparge)
    b.ingredient( Ingredient('hops','ekg','2.0') )
    """

    def __init__(self, subname=None, duration=None, **kwargs):
        super(Boil, self).__init__(**kwargs)        
        self.subname=( subname if subname else 'boil' )
        self.duration = None
        if (duration is not None):
            self.duration=Property('duration',duration)

    def solve(self):
        """ Calculate the bitterness and the volume at end of boil """
        pass #FIXME

    def end_state(self):
        self.solve()
        return({ 'wort_volume' : Quantity('9999gal'),
                 'IBU'         : Quantity('9999IBU') })

    def end_state_str(self):
        s = self.end_state()
        return('{0:s} with {1:s}\n'.format(s['wort_volume'],s['IBU']))
