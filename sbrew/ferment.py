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
        """ Calculate the ABV and attenuation based on OG and FG
        """
        if ('OG' in self.properties and
            'FG' in self.properties ):
            self.property('%ABV', Quantity(self.abv(),'%ABV') )
            self.property('atten', ((self.property('OG').to('sg')-self.property('FG').to('sg'))/(self.property('OG').to('sg')-1.0)*100.0), '%atten' )
        elif ('OG' in self.properties and
              'atten' in self.properties):
            fg = 1.0 + (self.property('OG').to('sg')-1.0) * self.property('atten')
            self.property('FG', Quantity(fg,'sg') )
            self.property('%ABV', Quantity(self.abv(),'%ABV') )
    
    def abv(self):
        """ Calculate the ABV and attenuation based on OG and FG

        The Complete Joy of Home Brewing, 3rd ed, p43
        ABW = OG-FG * 105, (where OG and FG in specific gravity)
        ABV = ABW * 1.25
        """
        return( (self.property('OG').to('sg') - self.property('FG').to('sg')) * 105 * 1.25 )

    def end_state_str(self):
        self.solve()
        if (not '%ABV' in self.properties):
            return(None)
        s = str(self.property('%ABV').quantity)
        if ('atten' in self.properties):
            s += ' (' + str(self.property('atten').quantity) + ')'
        return(s)
                                      

