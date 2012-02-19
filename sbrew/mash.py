from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity

class Mash(Recipe):
    """A mash is a simlpe recipe with no sub-steps.

    m =  Mash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print m
    """

    def __init__(self, name=None):
        self.name=None
        self.steps=[]
        self.subname=( name if name else 'mash' )
        self.ingredients=[]

    def name_with_default(self):
        """Return self.name with defaul of '' if None
        """
        return( self.name if self.name else '')

    def subname_with_default(self):
        """Return self.subname with defaul of 'mash' if None
        """
        return( self.subname if self.subname else 'mash')

    def total_type(self, type, unit=None):
        """Return total quantity of ingrdient with given type

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

    def total_grains(self):
        """Return total mass of grains
        """
        mass = self.total_type('grain')
        return( mass if mass else Mass('0lb'))

    def total_water(self):
        """Return total volume of water
        """
        vol = self.total_type('water')
        return( vol if vol else Quantity('0gal'))

    def add_mash(self, mash=None):
        """Add another mash into this mash
        """
        self.subname = self.subname_with_default() + ' + ' + mash.subname_with_default()
        for ingredient in mash.ingredients:
            self.ingredient( ingredient );
        self.combine_waters()

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

 
