from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from property import Property

class Beer(Recipe):
    """A placeholder recipe to express final details of beer
    """

    def __init__(self, subname=None, **kwargs):
        super(Beer, self).__init__(**kwargs)        
        self.subname=( subname if subname else 'beer' )
        self.import_property(kwargs, 'OG')

    def solve(self):
        """ Calculate the ABV and attenuation based on OG and FG
        """
        pass

    def end_state_str(self):
        self.solve()
        s = ''
        if ('%ABV' in self.properties):
            s += str(self.property('%ABV').quantity)
        return(s)
                                      

