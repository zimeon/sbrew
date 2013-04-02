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
        """Human readable output of this recipe

        A call with kwarg line_numbers will set off printing such that
        all subsequent steps will print line numbers.
        """
        if ('line_numbers' in kwargs):
            kwargs['state']={'num':0}
            del kwargs['line_numbers']
        str_list = []
        if (self.name):
            str_list.append("\n")
            str_list.append( self._str_line_num(kwargs) +
                             "== " + self.name + " ==\n")
        if (not ('skip_steps' in kwargs)):
            for step in self.steps:
                str_list.append(step.__str__(**kwargs))
        if (self.subname):
            str_list.append("= " + self.subname + " =\n")
        if (len(self.ingredients)>0):
            str_list.append("Ingredients:\n")
            for ingredient in self.ingredients:
                str_list.append(self._str_line_num(kwargs) +
                                ' ' + str(ingredient) + "\n")
        if (len(self.properties)>0):
            str_list.append("Properties:\n")
            for name in sorted(self.properties.keys()):
                if ('type' not in self.properties[name].extra or
                    self.properties[name].extra['type']!='system'):
                    str_list.append(self._str_line_num(kwargs) +
                                    ' ' + str(self.properties[name]) + "\n")
        end_str = self.end_state_str()
        if (end_str is not None and end_str != ''):
            str_list.append(' -> '+end_str)
        return(''.join(str_list))

    def _str_line_num(self, kwargs):
        """Return line number prefix or nothing"""
        if ('line_number' in kwargs):
            kwargs['line_number'] += 1
            return('[%03d] ' % (kwargs['line_number']))
        else:
            return('')

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

        recipe.ingredient('water','to drink','6gal')
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

    def property(self,p,quantity=None,unit=None,default=NoProperty,**kwargs):
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
                        return(Property(p,default))
                return(q)
            else:
                # set with values given
                name = p
                p = Property(name,quantity,unit,**kwargs)
        else:
            name = p.name
        self.properties[name]=p

    def has_properties(self,*args):
        """True if recipe has the properties listed, else false"""
        for property in args:
            if (property not in self.properties):
                return(False)
        return(True)

    def has_property(self,*arg):
        """Another name for has_properties()"""
        return(self.has_properties(*arg))        

    def add(self,step):
        """Add a step to this recipe
        """
        self.steps.append(step)

    def import_property(self, kwargs, name, new_name=None, input='start'):
        """Import property from previous recipe step based on kwargs

        Will take from recipe pass with kwarg name 'start' unless
        input is specified. Will use name in current recipe unless
        new_name is specified.
        """
        if (new_name is None):
            new_name = name
        if (input in kwargs and
            name in kwargs[input].properties):
            self.property( new_name, kwargs[input].property(name) )

    def solve(self, reverse=False):
        """Solve for missing data based on the sequence of steps
        
        By default works start to finish, but alternatively will try to 
        work backward from finish to start. This implementation is just
        for a container recipe with steps, no calculation for this recipe
        itself.
        """
        if (reverse):
            print "Trying to solve backward..."
            for step in reversed(self.steps):
                step.solve()
        else:
            print "Trying to solve forward..."
            for step in self.steps:
                step.solve()

    def end_state_str(self):
        """String describing the end state of this recipe step
        """
        return(None)
