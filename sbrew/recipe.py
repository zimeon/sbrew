"""A Recipe is a set of steps that may include other Recipes."""

from .ingredient import Ingredient
from .property import Property, NoProperty, MissingProperty


class MissingParam(Exception):
    """Class for exception in solve because of missing parameter."""

    def __init__(self, msg=None):
        """Initialize MissingParam exception with message."""
        self.msg = msg

    def __str__(self):
        """Return message string or default."""
        if (self.msg):
            return(self.msg)
        return('Missing parameter exception')


class Recipe(object):
    """Representation of a complete or partial recipe as a set of steps.

    A recipe has a set of ingredients (real stuff: grain, water, etc.) 
    and properties (non-stuff: temperature, etc.). It also has a set of 
    steps that are undertaken to complete the recipe. Each step is itself 
    a recipe. The notion of a recipe does not cater for things done in 
    parallel, the steps are a simple sequence.

    A recipe may have zero or more inputs (connected to the outputs of 
    other recipes), and may have zero or one output (connected to the
    input of another recipe). Splitting of the consituents of a recipe
    must be done as part of the recipe (e.g. in decoction mash).
    """

    DEFAULT_NAME=None

    def __init__(self, name=None, verbose=False, debug=False, 
                 start=None, **kwargs):
        """Initialize a Recipe object."""
        self.name=name or self.DEFAULT_NAME
        self.description=None
        self.verbose=verbose
        self.debug=debug
        # Local data for this recipe
        self.steps=[]
        self.ingredients=[]
        self.properties={}
        # Inputs from other recipes
        self.inputs=[]
        if (start):
            self.connect_input(start)
        # Output to another recipe
        self.output=None

    def connect_input(self, input_recipe):
        """Connect input_recipe output as input to this recipe.

        Makes bi-directional link between the two recipes.
        """
        print("connecting %s output to %s input" % (input_recipe.fullname,input_recipe.fullname))
        self.inputs.append(input_recipe)
        input_recipe.set_output(self)
        self.import_forward() #FIXME - do we want/need this? Should it be done just at solve() time?

    @property
    def name_with_default(self):
        """Return self.name with default of 'recipe' if None."""
        return( self.name if self.name else 'recipe' )

    @property
    def fullname(self):
        """Return best name we can get for this recipe."""
        return(self.name_with_default)

    def __str__(self, **kwargs):
        """Human readable output of this recipe.

        A call with kwarg line_numbers will set off printing such that
        all subsequent steps will print line numbers.
        """
        if ('line_numbers' in kwargs):
            kwargs['state']={'num':0}
            del kwargs['line_numbers']
        str_list = []
        if (len(self.steps)==0 or 'skip_steps' in kwargs):
            str_list.append("= " + self.name_with_default + " =\n")
        else:
            str_list.append("\n")
            str_list.append( self._str_line_num(kwargs) +
                             "== " + self.name_with_default + " ==\n")
            if (self.description):
                str_list.append("\n" + self.description + "\n\n")
            for step in self.steps:
                str_list.append(step.__str__(**kwargs))
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
            str_list.append(' -> '+end_str+"\n")
        return(''.join(str_list))

    def _str_line_num(self, kwargs):
        """Return line number prefix or nothing."""
        if ('line_number' in kwargs):
            kwargs['line_number'] += 1
            return('[%03d] ' % (kwargs['line_number']))
        else:
            return('')

    def __add__(self, other):
        """Add two partial recipes together, returning a new recipe.

        The steps of the second follow those of the first. The ingredients
        are combined. The properties of the second override those of the
        first.
        """
        sum = Recipe()
        sum.steps += self.steps
        sum.steps += other.steps
        sum.name = self.fullname + " + " + other.fullname
        sum.ingredients += self.ingredients
        sum.ingredients += other.ingredients
        sum.properties = self.properties.copy()
        sum.properties.update(other.properties)
        return(sum)

    def ingredient(self, i, name=None, quantity=None, unit=None,
                   *properties, **kv_properties):
        """Add ingredient to this recipe, or find ingredient matching i, name.

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

    def property(self, p, quantity=None, unit=None, default=NoProperty, **kwargs):
        """Add/get property to this recipe.

        This is getter and setter for the property p. Perhaps not
        properly pythonic but p=Property and quantity!=None implies set,
        otherwise get.

        Returns None or the value of default is there is no such property.
        If default is not set then a MissingParam exception is raised.
        """
        if (isinstance(p,Property)):
            name = p.name
        else:
            # need to create a Property instance
            if (quantity is None):
                q = self.properties.get(p)
                if (q is None):
                    if (default == NoProperty):
                        raise MissingParam("%s has no property %s (has %s)" % (self.fullname,p,self.properties.keys()))
                    elif (default is None):
                        # request it to return None in this case that property does not exist
                        return None
                    else:
                        # get quantity of this property (else None)
                        return(Property(p,default))
                return(q)
            else:
                # set with values given
                name = p
                p = Property(name,quantity,unit,**kwargs)
        # finally set named property 
        self.properties[name]=p

    def has_properties(self,*args):
        """True if recipe has the properties listed, else false."""
        for property in args:
            if (property not in self.properties):
                return(False)
        return(True)

    def has_property(self,*arg):
        """Another name for has_properties()."""
        return(self.has_properties(*arg))        

    def properties_str(self):
        """Short string of property names for this recipe."""
        str_list = []
        if (len(self.properties)>0):
            for name in sorted(self.properties.keys()):
                if ('type' not in self.properties[name].extra or
                    self.properties[name].extra['type']!='system'):
                    str_list.append(name)
        else:
            str_list.append("(no_properties)")
        return( ', '.join(str_list) )

    def add(self,step):
        """Add a step to this recipe.
        
        Adds step to the end of the list of steps.
        """
        self.steps.append(step)

    def import_property(self, name, new_name=None, source=None):
        """Import property from previous recipe step.

        Import an input property or an require output property from 
        a connected recipe. By default will look (in order) at all inputs
        for a matching name, otherwise a specific input or `output` may be 
        specified with the `source` parameter.

        Will use the same name in current recipe unless `new_name` is 
        specified.

        If there is no matching property then will silently return. Returns
        True for a successful import, False otherwise.
        """
        if (new_name is None):
            new_name = name
        if (source is None):
            for i in self.inputs:
                if (name in i.properties):
                    self.property( new_name, i.property(name) )
                    if (self.verbose):
                        print("imported %s and %s" % (name, new_name))
                    return True
        elif (source=='output'):
            if (self.output and name in self.output.properties):
                self.property( new_name, self.output.property(name) )
                if (self.verbose):
                    print("imported %s and %s" % (name, new_name))
                return True
        else: #source is an input Recipe instance
            if (name in source.properties):
                self.property( new_name, source.property(name) )
                if (self.verbose):
                    print("imported %s and %s" % (name, new_name))
                return True
        return False

    def set_output(self, output):
        """Set connection to recipe for which output of this recipe is and input.

        An output may only go to one other recipe so it is an error 
        to call this method if self.output is already set.
        """
        if (self.output is not None):
            raise Exception("Bad connection of %s -> %s, already connected to %s"%(self.name_with_default,output.name_with_default,self.output.name_with_default))
        self.output=output

    def import_forward(self):
        """Import properties from input(s)."""
        pass

    def import_backward(self):
        """Import output property requirements from output recipe."""
        pass

    def solve(self):
        """Solve for missing data based on the sequence of steps.
        
        By default works start to finish, but alternatively will try to 
        work backward from finish to start. This implementation is just
        for a container recipe with steps, no calculation for this recipe
        itself.

        Attempt to scan forward and backward up to the number of steps
        times.
        """
        solved = set()
        num_steps = len(self.steps)
        last_solved = 0
        attempt = 0
        for i in range(0,num_steps):
            attempt += 1
            print("Trying to solve, run %d ..." % (attempt))
            this_solved = 0 # number of steps solved this iteration
            for step in self.steps:
                if (step not in solved):
                    try:
                        step.import_forward()
                        step.import_backward()
                        step.solve()
                        print("solve: solved %s" % (step.fullname))
                        solved.add(step)
                        this_solved+=1
                    except LookupError as e:
                        print("solve: lookuperror in %s (%s)" % (step.fullname, str(e)))
                    except MissingParam as e:
                        print("solve: missing parameter(s) in %s (%s)" % (step.fullname, str(e)))
                    except MissingProperty as e:
                        print("solve: missing property in %s (%s)" % (step.fullname, str(e)))
                else:
                    this_solved+=1
            if (this_solved == last_solved):
                # no progress, exit
                break
            last_solved = this_solved
        # Did we finish?
        print("Out of %d steps, solved %d" % (num_steps,len(solved)))
        if (num_steps != len(solved)):
            if (self.debug):
                raise Exception("Failed to solve recipe")
            else:
                print("Failed to solve recipe (look at messages above)")
        else:
            print("Solved recipe")

    def end_state_str(self):
        """String describing the end state of this recipe step.

        Should always return a string, a simple question mark if no unseful information
        is available. Likely to be overridden in all specific implementations of
        Recipe.
        """
        return('')
