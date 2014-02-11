from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity

class Lauter(Recipe):
    """Lauter process: start with mash, extract wort

    l = Lauter()

    At the end of the lauter the key properties are 

    wort_volume - volume of wort extracted

    wort_gravity - gravity of the wort extracted
    """

    def __init__(self, **kwargs):
        """Initialize Lauter object which is a Recipe

        If not sub-classed to a more specific type then will get the subname 
        'lauter'.
        """
        #print "Lauter.__init__" + str(kwargs)
        super(Lauter, self).__init__(**kwargs)
        # Lauter specific things
        if (self.subname is None):
            self.subname='lauter'
        if ('type' in kwargs):
            self.type = kwargs['type']
            self.subname += ' (%s)' % self.type
        self.extra_info=None # extra info for end_state_str
        if ('start' in kwargs):
            self.import_property(kwargs,'total_grain','grain')
            self.import_property(kwargs,'total_water','water')
            self.import_property(kwargs,'total_points','total_points')

    def solve(self):
        """Blank, exception"""
        raise Exception("Need to override Lauter solve()")

    def end_state_str(self):
        s = ''
        wv = self.property('wort_volume')
        if (wv is not None):
            s += str(wv.quantity) + ' wort'
        wg = self.property('wort_gravity')
        if (wg is not None):
            s += ' at ' + str(wg.quantity)
        if (self.extra_info is not None):
            s += ' (' + self.extra_info + ')'
        if (s != ''):
            s += "\n"
        return(s)
