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
        self.property( 'boil_rate', Quantity('0.5gal/h') )
        self.property( 'dead_space', Quantity('0.5gal') )
        if (duration is not None):
            self.property( 'duration', Quantity(duration) )
        if ('lauter' in kwargs):
            l = kwargs['lauter']
            self.property('v_boil', l.property('wort_volume'))
            self.property('start_gravity', l.property('wort_gravity'))

    def solve(self):
        """ Calculate the bitterness and the volume at end of boil """
        v_end_boil = self.property('v_boil').to('gal') - \
                      self.property('boil_rate').to('gal/h') * self.property('duration').to('h')
        self.property('wort_volume', v_end_boil - self.property('dead_space').to('gal'), 'gal')
        sg = (self.property('start_gravity').to('sg') - 1.0)
        print "sg: %f" % sg
        self.property('OG', 1.0 + ( sg * self.property('v_boil').to('gal') / v_end_boil ), 'sg')
        self.property('IBU', Quantity('39.39IBU') )

    def end_state_str(self):
        self.solve()
        return('%s @ %s with %s\n' % (self.property('wort_volume').quantity,
                                      self.property('OG').quantity,
                                      self.property('IBU').quantity) )
                                      

