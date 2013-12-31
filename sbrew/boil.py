from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from property import Property
from recipe import MissingParam

import math

# Tinseth hop utilization:
#
# Utilization = f(G) x f(T)
# where: 
# f(G) = 1.65 x 0.000125^(G - 1) 
# f(T) = [1 - e^(-0.04 x T)] / 4.15
# with
# G is specific gravity
# T in is time in mins
# Utilization is 
#
# from Palmer:
# http://www.howtobrew.com/section1/chapter5-5.html
# from Tinseth:
# http://www.realbeer.com/hops/research.html
#
def tinseth_utilization(gravity,time):
    g = gravity.to('sg')
    t = time.to('min')
    fg = 1.65 * math.pow(0.000125,(g-1.0))
    ft = ( 1.0 - math.exp(-0.04 * t)) / 4.15
    return(fg*ft)

# IBUs from a boiling hop addition
#
# AAU = Weight (oz) x % Alpha Acids (whole number)
# IBU = AAU x U x 75 / Vrecipe
#
# from
# http://www.howtobrew.com/section1/chapter5-5.html
#
def ibu_from_boil(weight,aa,volume,gravity,time):
    aau = weight.to('oz') * aa.to('%AA')
    u = tinseth_utilization(gravity,time)
    return( aau * u * 75 / volume.to('gal') )

class Boil(Recipe):
    """A boil is a simple recipe with no sub-steps.

    b = Boil(start=sparge,duration="60min")
    b.ingredient( Ingredient('hops','ekg','2.0') )
    """

    def __init__(self, subname=None, duration=None, **kwargs):
        super(Boil, self).__init__(**kwargs)        
        self.subname=( subname if subname else 'boil' )
        self.property( 'boil_rate', Quantity('0.5gal/h'), type='system' )
        self.property( 'dead_space', Quantity('0.5gal'), type='system' )
        if (duration is not None):
            self.property( 'duration', Quantity(duration) )
        self.import_property(kwargs, 'wort_volume', 'boil_start_volume')
        self.import_property(kwargs, 'wort_gravity', 'start_gravity')

    def solve(self):
        """ Calculate the bitterness and the volume at end of boil

        Works only forward
        """
        print "boil-solve, have %s properties" % (self.properties.keys())
        # Volume - forward
        if (self.has_properties('start_gravity','boil_end_volume')):
            v_end_boil = self.property('boil_end_volume').to('gal')
            self.solve_volume_forward(v_end_boil)
        elif (self.has_properties('start_gravity','boil_start_volume','boil_rate','duration')):
            v_end_boil = self.property('boil_start_volume').to('gal') - \
                         self.property('boil_rate').to('gal/h') * self.property('duration').to('h')
            self.solve_volume_forward(v_end_boil)
        # backward
        elif (self.has_properties('OG','wort_volume','boil_rate','duration')):
            self.solve_volume_backward()
        else:
            raise MissingParam("Can't solve boil, have %s properties" % (self.properties.keys()))
        # Bitterness
        total_ibu = 0.0
        for i in self.ingredients:
            if (i.type == 'hops'):
                t = Quantity('60min')
                if ('duration' in i.properties):
                    t = i.properties['duration'].quantity
                else:
                    print "Warning  - no duration specified for %s hops, assuming %s" % (i.name,t)
                aa = Quantity('5%AA')
                if ('aa' in i.properties):
                    aa = i.properties['aa'].quantity
                else:
                    print "Warning  - no AA specified for %s hops, assuming %s" % (i.name,aa)
                ibu = self.ibu_from_addition(i.quantity,aa,t)
                #i.properties['AA']=Property('AA',Quantity(aa,'IBU'))
                total_ibu += ibu
        self.property('IBU', Quantity(total_ibu,'IBU') )

    def solve_volume_forward(self, v_end_boil):
        self.property('wort_volume', v_end_boil - self.property('dead_space').to('gal'), 'gal')
        sg = (self.property('start_gravity').to('sg') - 1.0)
        self.property('OG', 1.0 + ( sg * self.property('boil_start_volume').to('gal') / v_end_boil ), 'sg')

    def solve_volume_backward(self):
        """Solve for boil volumes starting from desired end state""" 
        print "boi-solve-back-start"
        self.property('boil_end_volume', self.property('wort_volume').to('gal') + 
                                         self.property('dead_space').to('gal'), 'gal')
        print "boi-solve-back-mid"
        print "bev " + str(self.property('boil_end_volume'))
        print "br  " + str(self.property('boil_rate').to('gal/hour'))
        print "dur " + str(self.property('duration'))
        bsv = self.property('boil_end_volume').to('gal') +\
              self.property('boil_rate').to('gal/hour') *\
              self.property('duration').to('h')
        print "boi-solve-back-mid2"
        self.property('boil_start_volume', 7.0, 'gal')
        print "boi-solve-back-mid3"
        og = (self.property('OG').to('sg') - 1.0)
        self.property('start_gravity', 1.0 + (og * self.property('boil_end_volume').to('gal') /
                                                   self.property('boil_start_volume').to('gal') ), 'sg' )
        print "boi-solve-back-end"

    def ibu_from_addition(self, weight, aa, time):
        """ IBU from a single hop addition at a particular time in a boil """
        return ibu_from_boil(weight,aa,self.property('boil_end_volume'),self.property('OG'),time)

    def end_state_str(self):
        #self.solve()
        s = ''
        if ('wort_volume' in self.properties):
            s += str(self.property('wort_volume').quantity)
        else:
            s += '?'
        if ('OG' in self.properties):
            s += ' @ %s' % str(self.property('OG').quantity)
        if ('IBU' in self.properties):
            s += ' with %s' % str(self.property('IBU').quantity)
        return( s + "\n")
