from ingredient import Ingredient
from property import Property

class Recipe(object):
    """Representation of a complete or partial recipe as a set of steps

    The notion of a recipe does not cater for things done in parallel, the
    steps are a simple sequence.
    """

    def __init__(self, name=None, subname=None, **kwargs):
        self.name=name
        self.steps=[]
        self.subname=subname
        self.ingredients=[]
        self.properties={}

    def name_with_default(self):
        """Return self.name with default of '' if None
        """
        return( self.name if self.name else '')

    def subname_with_default(self):
        """Return self.subname with defaul of 'mash' if None
        """
        return( self.subname if self.subname else 'mash')

    def __str__(self, **kwargs):
        str_list = []
        if (self.name):
            str_list.append("\n")
            str_list.append("== " + self.name + " ==\n")
        if (not ('skip_steps' in kwargs)):
            for step in self.steps:
                str_list.append(str(step))
        if (self.subname):
            str_list.append("= " + self.subname + " =\n")
        if (len(self.ingredients)>0):
            str_list.append("Ingredients:\n")
            for ingredient in self.ingredients:
                str_list.append(' ' + str(ingredient) + "\n")
        if (len(self.properties)>0):
            str_list.append("Properties:\n")
            for name in sorted(self.properties.keys()):
                str_list.append(' ' + str(self.properties[name]) + "\n")
        end_str = self.end_state_str()
        if (end_str is not None):
            str_list.append(' -> '+end_str)
        return(''.join(str_list))

    def __add__(self, other):
        """Add the partial recipes togerther, returning a new recipe
        """
        sum=Recipe()
        sum.steps+=self.steps
        sum.steps+=other.steps
        sum.name= self.name + " + " + other.name
        sum.ingredients+=self.ingredients
        sum.ingredients+=other.ingredients
        sum.properties+=self.properties
        sum.properties+=other.properties
        return(sum)

    def ingredient(self,i,name=None,quantity=None,unit=None):
        """Add ingredient to this recipe.

        r.ingredient(
        """
        if (not isinstance(i,Ingredient)):
            if (quantity is None):
                # Find ingredient matching, return quantity
                for ing in self.ingredients:
                    if (ing.type==i and ing.name==name):
                        return(ing.quantity)
                raise ValueError("Failed to find ingredient '%s', '%s'" % (i,name) )
            else:
                i = Ingredient(i,name,quantity,unit)
        self.ingredients.append(i)

    def property(self,p,quantity=None,unit=None):
        """Add/get property to this recipe.

        This is getter and setter for the property p. Perhaps not
        properly pythonic but p=Property of quantity!=None implies set,
        otherwise get.

        Returns None is there is no such property.
        """
        if (not isinstance(p,Property)):
            if (quantity is None):
                # get quantity of this property (else None)
                return(self.properties.get(p))
            else:
                # set with values given
                name = p
                p = Property(name,quantity,unit)
        else:
            name = p.name
        self.properties[name]=p

    def add(self,step):
        """Add a step to this recipe
        """
        self.steps.append(step)
     
    def end_state_str(self):
        """String describing the end state of this recipe step
        """
        return(None)
