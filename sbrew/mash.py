from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity

class Mash(Recipe):
    """A mash is a simple recipe with no sub-steps.

    m =  Mash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print m
    """

    DEFAULT_NAME='mash'

    def __init__(self, **kwargs):
        super(Mash,self).__init__(**kwargs)

    def lookup_grains(self):
        print "Lookup grains"
        for ingredient in self.ingredients:
            if (ingredient.type == 'grain'):
                pass

    def total_type(self, type, unit=None):
        """Return total quantity of ingredient with given type

        Will use the units of the first ingredient of the given 
        type found. Will return None is there are no ingredients
        of this type unless a default unit is specified.
        """
        total=( Quanity(0.0,unit) if unit else None)
        for ingredient in self.ingredients:
            if (ingredient.type == type):
                if (total):
                    total+=ingredient.quantity
                else:
                    total=Quantity(ingredient.quantity)
        return total
 
    def total_grains(self, total_mass=None):
        """Return total mass of grains
        """
        if (total_mass):
            # Want to set total mass, are all grains set as pct?
            num_not_pct=0
            for ingredient in self.ingredients:
                if (ingredient.type == 'grain'):
                    if (ingredient.quantity.unit != '%'):
                        num_not_pct+=1
            if (num_not_pct>0):
                print "can't set total as not all pct"
            else:
                for ingredient in self.ingredients:
                    if (ingredient.type == 'grain'):
                        ingredient.quantity.unit = total_mass.unit
                    ingredient.pct = ingredient.quantity.value
                    ingredient.quantity.value = total_mass.value * ingredient.quantity.value / 100.0
        # Now return total mass
        mass = self.total_type('grain')
        return( mass if mass else Mass('0lb'))

    def total_points(self):
        """Return total number of points estimated to be in grains if fully converted

        FIXME - currently dumb, uses 35.11ppg for MO for all
        """
        total_points = 0.0
        for ingredient in self.ingredients:
            if (ingredient.type == 'grain'):
                total_points += ingredient.quantity.to('lb') * 35.11
        return( Quantity(total_points,'points') )

    def total_water(self):
        """Return total volume of water
        """
        vol = self.total_type('water')
        return( vol if vol else Quantity('0gal'))

    def add_mash(self, mash=None):
        """Add another mash into this mash
        """
        self.name = self.name_with_default + ' + ' + mash.name_with_default
        for ingredient in mash.ingredients:
            self.ingredient( ingredient );
        #self.combine_waters()

    def combine_waters(self):
        """Combine multiple water ingredients into one

        Will use the units of the first water quantity found
        """
        water_total=None
        for ingredient in self.ingredients:
            if (ingredient.type == 'water'):
                if (water_total):
                    water_total+=ingredient.quantity
                else:
                    water_total=Quantity(ingredient.quantity)
                self.ingredients.remove(ingredient)
        self.ingredient( Ingredient('water','',water_total) )

    def solve(self):
        self.property('total_water', self.total_water())
        self.property('total_grain', self.total_grains())
        self.property('total_points', self.total_points())

    def end_state_str(self):
        self.solve()
        return('%s, %s, %s\n' %
               (self.property('total_grain').short_str(),
                self.property('total_water').short_str(),
                self.property('total_points').short_str() ))
