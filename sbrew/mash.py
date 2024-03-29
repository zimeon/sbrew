"""Base model for a Mash."""

from .recipe import Recipe, MissingParam, SolverFailed
from .ingredient import Ingredient
from .property import MissingProperty
from .quantity import Quantity


class Mash(Recipe):
    """A mash is a simple recipe with no sub-steps.

    m =  Mash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print(m)
    """

    DEFAULT_NAME = 'Mash'

    def __init__(self, **kwargs):
        """Initialize Mash as subclass of Recipe."""
        super(Mash, self).__init__(**kwargs)

    def total_type(self, type, unit=None):
        """Return total quantity of ingredient with given type.

        Will use the units of the first ingredient of the given
        type found. Will return None is there are no ingredients
        of this type unless a default unit is specified.
        """
        total = (Quantity(0.0, unit) if unit else None)
        for ingredient in self.ingredients:
            if (ingredient.type == type):
                if (total):
                    total += ingredient.quantity
                else:
                    total = Quantity(ingredient.quantity)
        return total

    def all_grains_percentage(self):
        """True if all grain quantities are expressed as a percentage.

        This is used to flag the need to calculate back to get weights
        based on parameters specified for a later part of the recipe.
        """
        num_not_pct = 0
        num_pct = 0
        for ingredient in self.ingredients:
            if (ingredient.type == 'grain'):
                if (ingredient.quantity.unit == '%'):
                    num_pct += 1
                else:
                    num_not_pct += 1
        return(num_pct > 0 and num_not_pct == 0)

    def grain_weights_from_total_and_percentages(self, total_mass=None):
        """Calculate weight for each grain given overall total."""
        if (total_mass is None):
            total_mass = self.property('total_grain').quantity
        total_pct = 0.0
        # Want to set total mass, are all grains set as pct?
        if (not self.all_grains_percentage()):
            print("can't set total as not all pct")
        else:
            for ingredient in self.ingredients:
                if (ingredient.type == 'grain'):
                    ingredient.quantity.unit = total_mass.unit
                    ingredient.pct = ingredient.quantity.value
                    ingredient.quantity.value = total_mass.value * ingredient.quantity.value / 100.0

    def total_grains(self, total_mass=None):
        """Return total mass of grains."""
        if (total_mass):
            self.grain_weights_from_total_and_percentages(total_mass)
        # Now return total mass
        mass = self.total_type('grain')
        return(mass if mass else Quantity('0lb'))

    def total_points(self):
        """Return total number of points estimated to be in grains if fully converted.

        FIXME - currently dumb, uses 35.11ppg for MO for all
        """
        total_points = 0.0
        for ingredient in self.ingredients:
            if (ingredient.type == 'grain'):
                total_points += ingredient.quantity.to('lb') * 35.11
        return(Quantity(total_points, 'points'))

    def total_water(self):
        """Return total volume of water."""
        vol = self.total_type('water')
        return(vol if vol else Quantity('0gal'))

    def color_units(self):
        """Calculate number of mash color units from grain colors (L).

        The number of color units is defined as the grain quantity (lbs) multiplied
        by the color of each grain (L), divided by the total water volume.

        Use Morey equation. See, for example, <http://brewwiki.com/index.php/Estimating_Color>

        FIXME - should be able to configure or perhaps switch equation automatically
        based on color range.
        """
        mcu = 0.0
        try:
            for ingredient in self.ingredients:
                if (ingredient.type == 'grain'):
                    mcu += ingredient.quantity.to('lb') * ingredient.property('color').to('L')
            mcu /= self.total_water().to('gal')
        except ZeroDivisionError:
            mcu = 0.0
        except AttributeError:
            mcu = 0.0
        except MissingParam:
            mcu = 0.0
        except MissingProperty:
            mcu = 0.0
        if (mcu > 0.0):
            # set property only if we have a real value
            self.property('MCU', Quantity(mcu, 'MCU'))
        return(Quantity(mcu, 'MCU'))

    def mash_volume(self):
        """Return volume of mash including both liquid and grain."""
        return(water_grain_volume(self.total_water(), self.total_grains()))

    def add_mash(self, mash=None):
        """Add another mash into this mash."""
        self.name = self.name_with_default + ' + ' + mash.name_with_default
        for ingredient in mash.ingredients:
            self.ingredient(ingredient)

    def solve(self):
        """Solve the Mash forward."""
        if (self.all_grains_percentage()):
            if ('total_grain' in self.properties):
                self.grain_weights_from_total_and_percentages()
            else:
                raise MissingParam("Cannot solve mash as have only grain ratios")
        self.property('total_water', self.total_water())
        self.property('total_grain', self.total_grains())
        self.property('total_points', self.total_points())
        if (self.has_properties('total_water', 'total_grain')):
            self.property('mash_volume', self.mash_volume())
        self.color_units()

    def end_state_str(self):
        """Summary tring for end state of Mash."""
        try:
            self.solve()
        except SolverFailed:
            pass
        tg = self.property('total_grain', default='?lb').short_str()
        tw = self.property('total_water', default='?gal').short_str()
        tp = self.property('total_points', default='?points').short_str()
        return('%s, %s, %s' % (tg, tw, tp))


# Functions

def water_grain_volume(water, grain):
    """Return volume of water and grain.

    See <http://www.howtobrew.com/appendices/appendixD-3.html> for numbers, use 1lb grain

    has volume of 10oz = 10/128
    """
    vol = water.to('gal') + grain.to('lb') * 10.0 / 128.0
    return(Quantity(vol, 'gal'))
