from recipe import Recipe
from ingredient import Ingredient
from quantity import Quantity
from property import Property
from recipe import MissingParam

import math


def tinseth_utilization(gravity,time):
    """Tinseth hop utilization:

    Utilization = f(G) x f(T)

    where: 

    f(G) = 1.65 x 0.000125^(G - 1) 
    f(T) = [1 - e^(-0.04 x T)] / 4.15

    with

    G is specific gravity
    T in is time in mins

    from Palmer:
    http://www.howtobrew.com/section1/chapter5-5.html
    from Tinseth:
    http://www.realbeer.com/hops/research.html
    """
    g = gravity.to('sg')
    t = time.to('min')
    fg = 1.65 * math.pow(0.000125,(g-1.0))
    ft = ( 1.0 - math.exp(-0.04 * t)) / 4.15
    return(fg*ft)

def ibu_from_boil(weight,aa,volume,gravity,time):
    """IBUs from a boiling hop addition

    AAU = Weight (oz) x % Alpha Acids (whole number)
    IBU = AAU x U x 75 / Vrecipe

    from http://www.howtobrew.com/section1/chapter5-5.html
    """
    aau = weight.to('oz') * aa.to('%AA')
    u = tinseth_utilization(gravity,time)
    return( aau * u * 75 / volume.to('gal') )

class Boil(Recipe):
    """A boil is a simple recipe with no sub-steps.

    b = Boil(start=sparge,duration="60min")
    b.ingredient( Ingredient('hops','ekg','2.0') )
    """

    DEFAULT_NAME='boil'

    def __init__(self, name=None, duration=None, **kwargs):
        super(Boil, self).__init__(name=name, **kwargs)        
        self.property( 'boil_rate', Quantity('0.5gal/h'), type='system' )
        self.property( 'dead_space', Quantity('0.5gal'), type='system' )
        if (duration is not None):
            self.property( 'duration', Quantity(duration) )

    def import_forward(self):
        self.import_property('wort_volume', 'boil_start_volume')
        self.import_property('wort_gravity', 'start_gravity')
        self.import_property('MCU')

    def import_backward(self):
        self.import_property('OG',source='output')

    def solve(self):
        """ Calculate the bitterness and the volume at end of boil

        Includes methods for both forward and backward calculations 
        """
        print "boil-solve, have %s properties" % (self.properties.keys())
        # Do we have any sugar?
        total_sugar_points = self.points_from_sugars()
        # Volume - forward
        if (self.has_properties('boil_start_volume','start_gravity','boil_end_volume')):
            v_end_boil = self.property('boil_end_volume').to('gal')
            self.solve_volume_forward(v_end_boil,total_sugar_points)
        elif (self.has_properties('boil_start_volume','start_gravity','boil_rate','duration')):
            v_end_boil = self.property('boil_start_volume').to('gal') - \
                         self.property('boil_rate').to('gal/h') * self.property('duration').to('h')
            self.property('boil_end_volume',Quantity(v_end_boil,'gal'))
            self.solve_volume_forward(v_end_boil,total_sugar_points)
        # backward
        elif (self.has_properties('OG','wort_volume','boil_rate','duration')):
            self.solve_volume_backward(total_sugar_points)
        elif (self.has_properties('OG','boil_end_volume','boil_rate','duration')):
            self.solve_volume_backward(total_sugar_points)
        else:
            raise MissingParam("Can't solve boil, have %s properties" % (self.properties.keys()))
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
                if ('aa' in i.properties):
                    aa = i.properties['aa'].quantity
                else:
                    print "Warning  - no AA specified for %s hops, assuming %s" % (i.name,aa)
                ibu = self.ibu_from_addition(i.quantity,aa,t)
                i.properties['IBU']=Property('IBU',Quantity(ibu,'IBU'))
                total_ibu += ibu
        self.property('IBU', Quantity(total_ibu,'IBU') )
        self.color()

    def solve_volume_forward(self, v_end_boil, total_sugar_points=0.0):
        """Solve forward based on end of boil volume

        If total_sugar_points is non zero then we simply increase the OG
        by this number of points divided by the final volume.
        """
        print "boil-solve_volume_forward start"
        self.property('wort_volume', v_end_boil - self.property('dead_space').to('gal'), 'gal')
        sg = (self.property('start_gravity').to('sg') - 1.0)
        self.property('OG', 1.0 + ( sg * self.property('boil_start_volume').to('gal') / v_end_boil + ( 0.001 * total_sugar_points / v_end_boil ) ), 'sg')
        print "boil-solve_volume_forward end"

    def solve_volume_backward(self, total_sugar_points=0.0):
        """Solve for starting boil volumes starting from desired end state

        FIXME - does not yet handle sugar addition
        """
        if (total_sugar_points > 0.0):
            raise Exception("FIXME - can't solve boil backwards with sugar")
        print "boi-solve-back-start"
        if ('boil_end_volume' in self.properties):
            self.property('wort_volume', self.property('boil_end_volume').to('gal') - 
                                         self.property('dead_space').to('gal'), 'gal')
        else:
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
        self.property('boil_start_volume', bsv, 'gal')
        print "boi-solve-back-mid3"
        og = (self.property('OG').to('sg') - 1.0)
        self.property('start_gravity', 1.0 + (og * self.property('boil_end_volume').to('gal') /
                                                   self.property('boil_start_volume').to('gal') ), 'sg' )
        print "boi-solve-back-end"

    def points_from_sugars(self):
        """Return number of points from all sugars additions
        
        FIXME - add various sugar types
        """
        tot = 0.0
        for i in self.ingredients:
            if (i.type == 'sucrose'):
                pts = i.quantity.to('lb') * 46.0 # 46ppg
                i.properties['points']=Property('points',pts,'points')
                tot += pts
            elif (i.type == 'dme'):
                # 46ppg
                pts = i.quantity.to('lb') * 43.0 # 43ppg 
                i.properties['points']=Property('points',pts,'points')
                tot += pts
        return(tot)

    def ibu_from_addition(self, weight, aa, time):
        """ IBU from a single hop addition at a particular time in a boil """
        return ibu_from_boil(weight,aa,self.property('boil_end_volume'),self.property('OG'),time)

    def color(self):
        """Calculate color after boil based on mash color units (MCU) at start

        Morey formula, see for example: <http://brewwiki.com/index.php/Estimating_Color>

        SRM_Color = 1.4922 * [MCU ^ 0.6859] 
        """
        if (self.has_properties('MCU','boil_start_volume','boil_end_volume')):
            # scale MCU based on boil-down, then use formula
            mcu = self.property('MCU').to('MCU') * self.property('boil_start_volume').to('gal') / self.property('boil_end_volume').to('gal') 
            srm = 1.4922 * ( mcu ** 0.6859 )
            self.property('SRM',Quantity(srm,'SRM'))

    def end_state_str(self):
        #self.solve()
        s = str(self.property('wort_volume',default='?gal').quantity)
        if ('OG' in self.properties):
            s += ' @ %s' % str(self.property('OG').quantity)
        if ('IBU' in self.properties):
            s += ' with %s' % str(self.property('IBU').quantity)
        return(s)
