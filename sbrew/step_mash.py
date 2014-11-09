from mash import Mash
from quantity import Quantity

class StepMash(Mash):
    """A step mash where ingredients may be added and temperatures changed

    """

    def __init__(self, name=None):
        super(StepMash,self).__init__()
        self.name=( name if name else 'step_mash' )
        self.steps=[]
        self.ingredients=[]

    def add_step(self, type, **extra):
        """Add step to the mash process

        In most cases we are doing the same sorts of things as an infusion
        mash, such as heating, waiting, etc. However, the key distinguishing
        parts are the abilities to split and to mix mashes (ie. take and 
        recombine decoctions).
        """
        extra['type']=type
        if (type == 'infuse'):
            self.steps.append(extra)
        elif (type == 'rest'):
            self.steps.append(extra)
        elif (type == 'boil'):
            self.steps.append(extra)
        elif (type == 'heat'):
            self.steps.append(extra)
        elif (type == 'adjust'):
            self.steps.append(extra)
        else:
            raise SbrewError('Unknown step type "{0:s}"'.format(type))

    def total_water(self):
        """Add up all water to return total volume"""
        total_water = Quantity('0.0gal')
        for step in self.steps:
            if ('type' in step and step['type']=='infuse' and
                'volume' in step):
                total_water += Quantity(step['volume'])
        return(total_water)  
