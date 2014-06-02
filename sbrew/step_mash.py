from decoction_mash import DecoctionMash

class StepMash(DecoctionMash):
    """A step mash, just a restricted version of DecoctionMash

    Currently we do nothing other than override the initialization
    to get the name...
    """

    def __init__(self, name=None):
        super(StepMash,self).__init__()
        self.name=None
        self.steps=[]
        self.subname=( name if name else 'step_mash' )
        self.ingredients=[]
