from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from property import Property

class Ferment(Recipe):
    """A fermentation is a simple recipe with no sub-steps.

    """

    def __init__(self, subname=None, duration=None, **kwargs):
        super(Ferment, self).__init__(**kwargs)        
        self.subname=( subname if subname else 'ferment' )
        if ('start' in kwargs):
            s = kwargs['start']
            self.property('OG', s.property('OG'))

    def solve(self):
        """ Calculate the ABV and atten based on OG and FG

        The Complete Joy of Home Brewing, 3rd ed, p43
        ABW = OG-FG * 105, (where OG and FG in specific gravity)
        ABV = ABW * 1.25 
        """
        if ('OG' in self.properties and
            'FG' in self.properties ):
            abv = (self.property('OG').to('sg') - self.property('FG').to('sg')) * 105 * 1.25
            self.property('%ABV', Quantity(abv,'%ABV') )

    def end_state_str(self):
        self.solve()
        if (self.property('%ABV',default=None) is None):
            return(None)
        return(str(self.property('%ABV').quantity))
                                      

