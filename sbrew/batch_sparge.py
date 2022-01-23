"""Model for Batch Sparge as specialization of Lauter."""
from .quantity import Quantity
from .lauter import Lauter
from .recipe import MissingParam


class BatchSparge(Lauter):
    """Batch sparge, a special type of lauter with two or more extracts.

    There are two properties that are essential to calculating
    how a batch sparge will work:

    v_dead - dead volume of mach tun. This is the volume of of fluid
      that is left if the mash tun is drained in the absence
      of any grain. This can be measured by filling the tun
      with water, draining it, and then measuring the quanity
      that remains (either by depth or draining via some other means).

    grain_water_retention - the volume of water, per unit mass of grain,
      that is left in the grain when the water is drained from a mash.
      The usual first approximation is ~0.55qt/lb.

    Provides a means to calculate backwards or forwards. Going
    from desired outcome we have:

    wort_volume - volume of the combined wort extract from the
      two runnings of the batch sparge.

    wort_gravity - gravity of the combined wort extracted from the
      two runnings of the batch sparge.

    extracts - number of extracts, defauls to 2 but may be more (or
      just 1 in which case we have a simple sparge)
    """

    DEFAULT_NAME = 'Batch sparge'

    def __init__(self, extracts=2, **kwargs):
        """Initialize BatchSparge object as type of Lauter.

        Key properties required:
           wort_volume - the desired wort volume

        Relies on parameters of the system:
           v_dead - dead volume in tun when draining
           grain_water_retention
        """
        super(BatchSparge, self).__init__(**kwargs)
        # FIXME - should come from config and be realistic!
        self.v_dead = Quantity('0.25gal')
        self.grain_water_retention = Quantity('0.55qt/lb')  # qt/lb
        self.extracts = extracts

    def extractions_calculated_forward(self, v_water, v_in_grain, v_wort):
        """Calculate volumes and points for the set of extractions calculated forward.

        Assumes that v_water, v_in_grain, v_wort are values in gallons.

          v_water - total volume of water in mash at start of sparge
          v_in_grain - volume of water stuck in grain after draining
          v_wort - total runnings to be collected (hence volume at start of boil)

        and relies upon settings:

          self.extracts - the number of extracts (default 2)

        and uses:

          v_stuck - volume that will be stuck in grain and any dead volume
          v_first - volume of first runnings etc.

        Returns two lists:
          vols - a list of volumes extracted
          points - a list of fractions of the starting points extracted

        Thus sum(points)<1.0 for all practical situations (==1 for no v_in_grain and
        no dead volume).

        Key assumption is that the point (sugars) are distributed evenly
        between all the water portions: drained out and left in the grain
        and dead space.
        """
        v_stuck = v_in_grain + self.v_dead.to('gal')
        v_first = v_water - v_stuck
        v_rest = v_wort - v_first
        # assume points equally distributed in free water and grain
        p_first = v_first / (v_first + v_stuck)
        p_rest = (1 - p_first)
        if (v_rest < 0.0):
            raise Exception(
                "Requested boil volume is less than first runnings")
        vols = [v_first]
        points = [p_first]
        if (self.extracts > 1):
            v_each = v_rest / (self.extracts - 1)
            for n in range(1, self.extracts):
                # add and sparge v_each for remaining sparges
                if (v_rest < 0.000001):
                    p_this = 0.0
                    p_rest = 0.0
                else:
                    # assume remaining points equally distributed
                    frac_drained = v_each / (v_each + v_stuck)
                    p_this = p_rest * frac_drained
                    p_rest = p_rest * (1 - frac_drained)
                vols.append(v_each)
                points.append(p_this)
        return(vols, points)

    def solve(self):
        """Solve based on what is known."""
        if (self.has_properties('grain', 'water',
                                'total_points', 'wort_volume') or
                self.has_properties('grain', 'water', 'total_points',
                                    'boil_start_volume')):
            return(self.solve_from_mash_and_desired_volume())
        else:
            raise MissingParam("Bad properties to solve batch sparge "
                               "(have %s)" % self.properties_str())

    def solve_from_mash_and_desired_volume(self):
        """Solve to get gravity of extracted wort.

        Must know the results of the mash (volume and total points)
        and also the desired volume (wort_volume). Will assume an
        equal volume in first and second runnings.
        """
        if (self.has_property('wort_volume')):
            wort_volume = self.property('wort_volume').to('gal')
        elif (self.has_property('boil_start_volume')):
            wort_volume = self.property('boil_start_volume').to('gal')
            self.property('wort_volume', wort_volume, 'gal')
        else:
            raise MissingParam('Need either wort_volume or boil_start_volume')
        # calculate sparge with a total of self.extracts steps
        v_wort = wort_volume
        v_water = self.property('water').to('gal')
        v_in_grain = self.property('grain').to('lb') *\
            self.grain_water_retention.to('qt/lb') / 4.0
        vols, points = self.extractions_calculated_forward(
            v_water, v_in_grain, v_wort)
        # description of process
        t_points = self.property('total_points').to('points')
        if (self.extracts == 2):
            # special formatting for case of normal batch sparge
            self.extra_info = 'first runnings: %s at %s; second runnings %s at %s; efficiency %.1f%%' %\
                (Quantity(vols[0], 'gal'), Quantity(1.0 + 0.001 * points[0] * t_points / vols[0], 'sg'),
                 Quantity(vols[1], 'gal'), Quantity(
                     1.0 + 0.001 * points[1] * t_points / vols[1], 'sg'),
                 (sum(points) * 100.0))
        else:
            # 1,3,4...
            e_strs = []
            for n in range(0, self.extracts):
                e_str = "%s at %s" % (Quantity(vols[n], 'gal'),
                                      Quantity(1.0 + 0.001 * points[n] * t_points / vols[n], 'sg'))
                e_strs.append(e_str)
            self.extra_info = '%d way batch sparge: %s; efficiency %.1f%%' %\
                (self.extracts, '; '.join(e_strs), (sum(points) * 100.0))
        # final values
        wort_gravity = 1.0 + 0.001 * sum(points) * t_points / v_wort
        self.property('wort_gravity', Quantity(wort_gravity, 'sg'))
        self.property('wort_volume', Quantity(sum(vols), 'gal'))
