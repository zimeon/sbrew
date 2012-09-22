from mash import Mash
from quantity import Quantity
from sbrew_error import SbrewError
#from brewtime import BrewTime
from datetime import timedelta

class DecoctionMash(Mash):
    """A decoction mash, derived from a simple mash.

    m =  DecoctionMash()
    m.ingredient( Ingredient('grain','belgian pilsner','9.75lb') )
    m.ingredient( Ingredient('grain','caravieene belgian','1.25lb') )
    m.ingredient( Ingredient('grain','clear candi sugar','0.87lb') )
    print m
    """

    def __init__(self, name=None):
        super(DecoctionMash,self).__init__()
        self.name=None
        self.steps=[]
        self.subname=( name if name else 'decoction_mash' )
        self.ingredients=[]

    def add_step(self, type, **extra):
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
        elif (type == 'split'):
            decoction = DecoctionMash()
            extra['decoction']=decoction
            self.steps.append(extra)
            return(decoction)     
        elif (type == 'mix'):
            self.steps.append(extra)
        elif (type == 'heat'):
            self.steps.append(extra)
        elif (type == 'heat'):
            self.steps.append(extra)
        else:
            raise SbrewError('Unknown step type for decoction mash "{0:s}"'.format(type))

    def add_rest(self,time):
	return add_step('rest',time=time)
 
    def __str__(self):
        # Use superclass str() but don't try to render steps
        s = super(DecoctionMash,self).__str__(skip_steps=1)
        # Now render the steps in our own special way
        s += '***steps***\n'
        s += self.steps_str()
        return(s)

    def steps_str(self,start_time=timedelta(),n=0,indent=''):
	""" Write out a time sequence of all steps, including decoctions

        Goal is to create a useful presentation of all steps on a single 
	timeline, including working out any implied rests because the 
	decoction steps take longer than explicit steps in the main mash.
        """
        # Go through the sequence of steps in this mash and any decoctions
        # taken to populate the set of stages for each.
        stages = {}
        self.find_stages(stages)
        # Now set up pointers into each set a stages 
        mashes = sorted(stages.keys()) 
        stages_iter={}
        stages_next={} 
        stages_started={}
        s = "H:MM:SS "
        for mash in mashes:
            s += "| {0:27s} ".format(mash)
            stages_iter[mash]=iter(stages[mash])
            stages_next[mash]=stages_iter[mash].next()
            stages_started[mash]=0
        s += '\n'
        # Keep looking at all lists of stages to find next time, exit when all done
        while True:
            # Find lowest time in nexts
            t = timedelta(days=9999) #big
            for mash in mashes:
                #tt = (str(stages_next[mash]['time']) if stages_next[mash] else 'none')
                #s += 'test {0:s} has time {1:s}\n'.format(mash,tt)
                if (stages_next[mash] and stages_next[mash]['time']<t):
                    t = stages_next[mash]['time']
            # Output all things that happen at time t
            s += "{0:s} ".format(t)
            for mash in mashes:
                state = ''
		if (stages_next[mash]):
                    if (stages_next[mash]['time']<=t):
                        state = self.stage_state_str(stages_next[mash])
                        stages_started[mash]+=1
                        try:
                            stages_next[mash]=stages_iter[mash].next()
                        except StopIteration:
                            stages_next[mash]=None
                    elif (stages_started[mash]>0):
                        state = '    -ditto-'
                    else:
			state = '' # '-not-started-'
                else:
                    state = '' # '-end-'
                s += "| {0:27s} ".format(state)
            s += '\n'
            # Are we done? All iterators used up
            not_none=0;
            for mash in mashes:
                if (stages_next[mash]):
                    not_none += 1
            if (not_none==0):
                break
        return(s)

    def stage_state_str(self,stage):
        str = "{0:s} @ {1:s} ".format(stage['volume'],stage['temp'])
        return(str)

    def find_stages(self, stages, mash_name='_main', start_time=timedelta()):
        # Create list for this mash's stages in main stages dict, clear
        stage=[]
        stages[mash_name]=stage
        #
        t = start_time
        vol = Quantity('0gal')
        temp = Quantity()
        mix_time = None
        num = 0;
	for step in self.steps:
            num += 1
            type = step['type']
            if (type == 'mix'):
                if (t < mix_time):
                    t = mix_time
            # Current state
            if (num>1):
                stage.append({'type': 'state', 'time': t, 'volume': vol, 'temp': temp})
            if ('volume' in step):
                vol=step['volume']
            if ('temp' in step):
                temp=step['temp']
            # Action of this step
            action = {}
            action.update(step)
            action['time']=t
            if ('time' in step):
                t += self.parsetime(step['time']) 
            if (type == 'split'):
                mix_time = t + step['decoction'].total_time()
                decoction_name = ( step['name'] if ('name' in step) else 'decoction' )      
                step['decoction'].find_stages(stages, decoction_name, t)
        # no return val, data left in stages  

    def parsetime(self, tstr):
        tqty = Quantity(tstr)
        if (tqty.unit == 'min'):
            return(timedelta(minutes=tqty.value))
        else:
	    raise SbrewError('Unknow time unit "{0:s}"'.format(tqty.unit))

    def total_time(self):
        """Return the total time that this mash takes to complete.
 
        Doesn't deal with decoctions but is useful to calculate the time
        of a decoction which is part of a main mash.
	"""
        t = timedelta()
	for step in self.steps:
            if ('time' in step):
                t += self.parsetime(step['time']) 
        return(t)
      
