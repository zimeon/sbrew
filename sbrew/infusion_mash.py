from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity
from mash import Mash

class InfusionMash(Mash):
    """A single step infusion mash

    m =  Mash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print m
    """

    def __init__(self, **kwargs):
        super(Mash, self).__init__(**kwargs)
        #self.subname=( name if name else 'mash' )
