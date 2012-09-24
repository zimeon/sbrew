from mass import Mass
from quantity import Quantity
from lauter import Lauter

class BatchSparge(Lauter):
    """Batch sparge, a special type of lauter

    """

    def __init__(self, **kwargs):
        """

        Parameters required:
        """
        print "batch sparge __init__" + str(kwargs)
        super(BatchSparge, self).__init__(**kwargs)
        self.name='batch sparge'
        self.wort_volume = Quantity('6.75gal')
        self.wort_gravity = None #don't know yet
        self.v_dead = Quantity('0.25gal')
        self.grain_water_retention = Quantity('0.55qt/lb') # qt/lb
        
    def extraction(self,v_boil,v_stuck,v_first):
        """Efficiency and extraction of batch sparge

        All parameters are just numbers
        """
        v_second = v_boil-v_first
        # assume points equally distributed in free water and grain
        p_first  = v_first/(v_first+v_stuck)
        # assume remaining points equally distributed
        p_second = (1-p_first)*v_second/(v_second+v_stuck)
        return( p_first, p_second, v_second )

    def solve(self):
        """Solve to get size and gravity of extracted wort

        Also give size and gravity of the two runnings.
        """
        v_wort = self.wort_volume.to('gal')
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
        self.wort_gravity = 1.0 + 0.001 * (p_first+p_second) * t_points / v_wort
        self.wort_gravity=Quantity(self.wort_gravity,'sg')

