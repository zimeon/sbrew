from ingredient import Ingredient
from property import Property

class NoProperty(object):
    """Class used to represent 'no property' default"""
    def __str__(self):
        return('NoProperty')

class Recipe(object):
    """Representation of a complete or partial recipe as a set of steps

    A recipe has a set of ingredients (real stuff: grain, water, etc.) 
    and properties (temperature, etc.). It also has a set of steps that
    are undertaken to complete the recipe. Each step is itself a recipe.
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
        return( self.name if self.name else '' )

    def subname_with_default(self):
        """Return self.subname with default of 'recipe' if None
        """
        return( self.subname if self.subname else 'recipe' )

    def fullname(self):
        """Return best name we can get for this recipe
        """
        if ( self.name is None ):
            return(self.subname_with_default())
        elif ( self.subname is None ):
            return(self.name)
        else:
            return(self.name + '(' + self.subname + ')')

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
        if (end_str is not None and end_str != ''):
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

    def ingredient(self,i,name=None,quantity=None,unit=None,*properties,**kv_properties):
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
                i = Ingredient(i,name,quantity,unit,*properties,**kv_properties)
        self.ingredients.append(i)

    def property(self,p,quantity=None,unit=None,default=NoProperty):
        """Add/get property to this recipe.

        This is getter and setter for the property p. Perhaps not
        properly pythonic but p=Property of quantity!=None implies set,
        otherwise get.

        Returns None or the value of default is there is no such property.
        If default is not set the a message is printed.
        """
        if (not isinstance(p,Property)):
            if (quantity is None):
                q = self.properties.get(p)
                if (q is None):
                    if (default == NoProperty):
                        print "%s has no property %s (has %s)" % (self.fullname(),p,self.properties.keys())
                        return(None)
                    else:
                        # get quantity of this property (else None)
                        return(default)
                return(q)
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
