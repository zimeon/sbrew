from mass import Mass
from quantity import Quantity
from lauter import Lauter
from recipe import MissingParam

class BatchSparge(Lauter):
    """Batch sparge, a special type of lauter with two extracts

    There are two properties that are essential to calculating
    how a batch sparge will work:

    v_dead - dead volume of mach tun. This is the volume of of fluid
      that is left if the mash tun is drained in the absence
      of any grain. This can be measured by filling the tun
      with water, draining it, and then measuring the quanity
      that remains (either by depth or draining via some other means).

    grain_water_retention - the volume of water, per unit mass of grain, 
      that is left in the grain when the water is drained from a mash.
      The usual first approximation is 0.5qt/lb.
      
    Provides a means to calculate backwards or forwards. Going 
    from desired outcome we have:

    wort_volume - volume of the combined wort extract from the
      two runnings of the batch sparge.

    wort_gravity - gravity of the combined wort extracted from the
      two runnings of the batch sparge.

    """

    DEFAULT_NAME='batch sparge'

    def __init__(self, **kwargs):
        """Initialize BatchSparge object as type of Lauter

        Key properties required:
           wort_volume - the desired wort volume
           
        Relies on parameters of the system:
           v_dead - dead volume in tun when draining
           grain_water_retention 
        """
        super(BatchSparge, self).__init__(**kwargs)
        self.v_dead = Quantity('0.25gal')
        self.grain_water_retention = Quantity('0.55qt/lb') # qt/lb
        
    def extraction(self,v_boil,v_stuck,v_first):
        """Efficiency and extraction of batch sparge

        All parameters are just numbers (not Quantity values) where only
        the ratios are important. Obviously they must all be expressed in
        the same units.

          v_boil - total runnings collected (hence volume at start of boil)
          v_stuck - volume that will be stuck in gran and any dead volume
          v_first - volume of first runnings

        The results are:

          p_first - fraction of total points in first runnings
          p_second - fraction of total points in second runnings
          v_second - volume of second runnings

        where

          p_first + p_second <= 1.0 

        because of the points left in v_stuck.
        """
        v_second = v_boil-v_first
        # assume points equally distributed in free water and grain
        p_first  = v_first/(v_first+v_stuck)
        # assume remaining points equally distributed
        p_second = (1-p_first)*v_second/(v_second+v_stuck)
        return( p_first, p_second, v_second )

    def solve(self):
        """Solve based on what is known
        """
        if (self.has_properties('grain','water','total_points','wort_volume') or
            self.has_properties('grain','water','total_points','boil_start_volume')):
            return( self.solve_from_mash_and_desired_volume() )
        else:
            raise MissingParam("Bad properties to solve batch sparge (have %s)" % self.properties_str())
     
    def solve_2(self):
        """Solve to get size and gravity of extracted wort

        Also give size and gravity of the two runnings.
        """
        wort_volume = self.property('boil_start_volume').to('gal') - self.v_dead.to('gal')
        self.property('wort_volume',wort_volume,'gal')
        # calculate sparge
        v_wort = wort_volume
        v_water = self.property('water').to('gal')
        v_in_grain = self.property('grain').to('lb') *\
                     self.grain_water_retention.to('qt/lb') / 4.0
        v_first = v_water - v_in_grain
        v_stuck = v_in_grain + self.v_dead.to('gal')
        p_first, p_second, v_second = self.extraction(v_wort,v_stuck,v_first)
        # description of process
        t_points = self.property('total_points').to('points')
        self.extra_info = 'first runnings: %s at %s; second runnings %s at %s; efficiency %.1f%%' %\
            (Quantity(v_first,'gal'),Quantity(1.0 + 0.001 * p_first * t_points / v_first, 'sg'),\
             Quantity(v_second,'gal'),Quantity(1.0 + 0.001 * p_second * t_points / v_second, 'sg'),\
             ((p_first+p_second) * 100.0) )
        # final values
        wort_gravity = 1.0 + 0.001 * (p_first+p_second) * t_points / v_wort
        self.property('wort_gravity', Quantity(wort_gravity,'sg'))
        self.property('wort_volume', Quantity(v_first+v_second,'gal'))

    def solve_from_mash_and_desired_volume(self):
        """Solve to get gravity of extracted wort

        Must know the results of the mash (volume and total points)
        and also the desired volume (wort_volume). Will assume an 
        equal volume in first and second runnings.
        """
        if (self.has_property('wort_volume')):
            wort_volume = self.property('wort_volume').to('gal')
        elif (self.has_property('boil_start_volume')):
            # FIXME, this seems wrong
            wort_volume = self.property('boil_start_volume').to('gal') - self.v_dead.to('gal')
            self.property('wort_volume',wort_volume,'gal')
        else:
            raise MissingParam('bwaa')
        # calculate sparge
        v_wort = wort_volume
        v_water = self.property('water').to('gal')
        v_in_grain = self.property('grain').to('lb') *\
                     self.grain_water_retention.to('qt/lb') / 4.0
        v_first = v_water - v_in_grain
        v_stuck = v_in_grain + self.v_dead.to('gal')
        p_first, p_second, v_second = self.extraction(v_wort,v_stuck,v_first)
        # description of process
        t_points = self.property('total_points').to('points')
        self.extra_info = 'first runnings: %s at %s; second runnings %s at %s; efficiency %.1f%%' %\
            (Quantity(v_first,'gal'),Quantity(1.0 + 0.001 * p_first * t_points / v_first, 'sg'),\
             Quantity(v_second,'gal'),Quantity(1.0 + 0.001 * p_second * t_points / v_second, 'sg'),\
             ((p_first+p_second) * 100.0) )
        # final values
        wort_gravity = 1.0 + 0.001 * (p_first+p_second) * t_points / v_wort
        self.property('wort_gravity', Quantity(wort_gravity,'sg'))
        self.property('wort_volume', Quantity(v_first+v_second,'gal'))

