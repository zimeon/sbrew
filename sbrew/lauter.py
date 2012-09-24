from recipe import Recipe
from ingredient import Ingredient
from mass import Mass
from quantity import Quantity

class Lauter(Recipe):
    """Lauter process: start with mash, extract wort

    l = Lauter()
    """

    def __init__(self, **kwargs):
        print "Lauter.__init__" + str(kwargs)
        super(Lauter, self).__init__(**kwargs)
        # Lauter specific things
        if (self.subname is None):
            self.subname='lauter'
        if ('type' in kwargs):
            self.type = kwargs['type']
            self.subname += ' (%s)' % self.type
        self.wort_volume=None
        self.wort_gravity=1.0
        self.extra_info=None # extra info for end_state_str
        if ('mash' in kwargs):
            m = kwargs['mash']
            self.property('grain',m.property('total_grain'))
            self.property('water',m.property('total_water'))
            self.property('total_points',m.property('total_points'))

    def __str2__(self):
        s = ""
        s += "grain %s, water %s" % (self.property('grain'), self.property('water')) 
        return(s)

    def end_state_str(self):
        s = ''
        if (self.wort_volume is not None):
            s += '{0:s} wort at {1:s}'.format(str(self.wort_volume),str(self.wort_gravity))
        if (self.extra_info is not None):
            s += ' (' + self.extra_info + ')'
        if (s != ''):
            s += "\n"
        return(s)
