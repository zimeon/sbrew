from ingredient import Ingredient

class Recipe(object):
    """Representation of a complete or partial recipe as a set of steps

    The notion of a recipe does not cater for things done in parallel, the
    steps are a simple sequence.

    r = Recipe("mash")
    r.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    r.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    r.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print r
    """

    def __init__(self, name=None):
        self.name=name
        self.steps=[]
        self.subname=None
        self.ingredients=[]

    def __str__(self, **kwargs):
        str_list = []
        if (self.name):
            str_list.append("== " + self.name + " ==\n")
        if (not ('skip_steps' in kwargs)):
            for step in self.steps:
                str_list.append(str(step))
        if (self.subname):
            str_list.append("= " + self.subname + " =\n")
        for ingredient in self.ingredients:
            str_list.append('' + str(ingredient) + "\n")
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
        return(sum)

    def ingredient(self,i):
        """Add ingredient to this recipe.
        """
        self.ingredients.append(i)

    def add(self,step):
        """Add a step to this recipe
        """
        self.steps.append(step)
     
