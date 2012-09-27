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
        # Volume
        v_end_boil = self.property('v_boil').to('gal') - \
                     self.property('boil_rate').to('gal/h') * self.property('duration').to('h')
        self.property('wort_volume', v_end_boil - self.property('dead_space').to('gal'), 'gal')
        sg = (self.property('start_gravity').to('sg') - 1.0)
        self.property('OG', 1.0 + ( sg * self.property('v_boil').to('gal') / v_end_boil ), 'sg')
        # Bitterness
        total_ibu = 0.0
        for i in self.ingredients:
            if (i.type == 'hops'):
                t = Quantity('60min')
                if ('time' in i.properties):
                    t = i.properties['time'].quantity
                else:
                    print "Warning  - no time specified for %s hops, assuming %s" % (i.name,t)
                aa = Quantity('5%AA')
                if ('AA' in i.properties):
                    aa = i.properties['AA'].quantity
                else:
                    print "Warning  - no AA specified for %s hops, assuming %s" % (i.name,aa)
                ibu = self.ibu_from_addition(aa,t)
                i.properties['%AA']=Property('%AA',Quantity(aa,'IBU'))
                total_ibu += ibu
        self.property('IBU', Quantity(total_ibu,'IBU') )

    def ibu_from_addition(self, aa, time):
        return(1.2)

    def end_state_str(self):
        self.solve()
        return('%s @ %s with %s\n' % (self.property('wort_volume').quantity,
                                      self.property('OG').quantity,
                                      self.property('IBU').quantity) )
                                      

