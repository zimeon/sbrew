from .mash import water_grain_volume
from .step_mash import StepMash
from .recipe import MissingParam
from .quantity import Quantity
from .ingredient import Ingredient

from datetime import timedelta

class DecoctionMash(StepMash):
    """A decoction mash, an extension of a step mash to split/mix decoctions.

    As a specialization of the step mash the steps are a dict of instructions
    for the step rather than a full recipe.

    m =  DecoctionMash()
    m.ingredient( Ingredient('grain','pilsner','5lb') )
    m.ingredient( Ingredient('grain','wheat malt','5lb') )
    m.add_step('infuse',volume='3.6gal',temp='108F')
    m.add_step('heat',temp='122F',time='10min')
    m.add_step('rest',time='15min')
    d1=m.split(time='5min',remove='40%')
    d1.add_step('heat',temp='160F',time='15min')
    d1.add_step('rest',time='15min')
    d1.add_step('heat',temp='212F',time='15min')
    d1.add_step('boil',time='20min')
    m.mix(decoction=d1,time='10min')
    m.add_step('adjust',temp='147F')
    m.add_step('rest',time='20min')
    print(m)
    """

    DEFAULT_NAME='decoction mash'

    def __init__(self, **kwargs):
        super(DecoctionMash,self).__init__(**kwargs)
        self.steps=[]
        self.ingredients=[]

    def split(self,**extra):
        """Split mash to take decoction

        Add 'split' step and returns the new DecoctionMash object. The split
        must be a fraction.
        """
        decoction = DecoctionMash(name="decoction")
        try:
            frac = Quantity(extra['remove']).to('fraction') #FIXME - implement volume
        except Exception as e:
            raise MissingParam("Must specify remove fraction when splitting decoction: %s" % (str(e)))
        extra['frac'] = frac
        # Take portion of volume from this mash, put into decoction
        extra['type'] = 'split'
        extra['decoction'] = decoction
        for ingredient in self.ingredients:
            q = ingredient.quantity * frac
            #ingredient.quantity -= q  #FIXME - should really split and mix in
            i = Ingredient( ingredient.type, ingredient.name, q )
            decoction.ingredient(i)
        self.steps.append(extra)
        return(decoction)

    def mix(self,decoction,**extra):
        """Mix decoction into this mash

        Add a 'mix' step that integrates the decoction mash into this mash
        """
        extra['type'] = 'mix'
        extra['decoction'] = decoction
        self.steps.append(extra)

    def __str__(self):
        # Use superclass str() but don't try to render steps
        s = super(DecoctionMash,self).__str__(skip_steps=1)
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
            s += "| %-27s " % (mash)
            stages_iter[mash]=iter(stages[mash])
            stages_next[mash]=next(stages_iter[mash])
            stages_started[mash]=0
        s += '\n'
        # Keep looking at all lists of stages to find next time, exit when all done
        ditto = {}
        while True:
            # Find lowest time in nexts
            t = timedelta(days=9999) #big
            for mash in mashes:
                #tt = (str(stages_next[mash]['time']) if stages_next[mash] else 'none')
                if (stages_next[mash] and stages_next[mash]['time']<t):
                    t = stages_next[mash]['time']
            # Output all things that happen at time t
            state_line = "%7s " % t
            step_line  = "        "
            step_type = ''
            for mash in mashes:
                state = ''
                if (stages_next[mash]):
                    if (stages_next[mash]['time']<=t):
                        state = self.stage_state_str(stages_next[mash])
                        if ('type' in stages_next[mash]):
                            step_type = stages_next[mash]['type']
                        stages_started[mash]+=1
                        try:
                            stages_next[mash]=next(stages_iter[mash])
                        except StopIteration:
                            stages_next[mash]=None
                        if (mash in ditto):
                            del ditto[mash]
                    elif (stages_started[mash]>0):
                        if (mash in ditto):
                            state = '|'
                        else:
                            state = self.stage_state_str(stages_next[mash])
                        ditto[mash] = 1
                    else:
                        state = '' # '-not-started-'
                else:
                    state = '' # '-end-'
                state_line += "  %-27s " % state
                step_line  += "  %-27s " % ('| '+step_type)
            s += state_line + '\n' + step_line+ "\n"
            # Are we done? All iterators used up
            not_none=0;
            for mash in mashes:
                if (stages_next[mash]):
                    not_none += 1
            if (not_none==0):
                break
        return(s)

    def stage_state_str(self,stage):
        str = "%s @ %s " % (stage['volume'],stage['temp'])
        return(str)

    def find_stages(self, stages, mash_name='_main', start_time=timedelta()):
        """Create list for this mash's stages in main stages dict

        The stages dict has a set of stages for the main mash ('_main') and
        for any decoctions. The goal is to work these out with the same set of 
        time boundaries so that they can be displayed in parallel. All times
        are measured from the start_time (0 if not given).
        """
        stage=[]
        stages[mash_name]=stage
        # running variables
        t = start_time
        water = self.total_type('water','gal') #ingredients only
        print("find_stages: %s %s" % (mash_name, str(water)))
        vol = Quantity('0gal')
        temp = Quantity()
        mix_time = Quantity('0min')
        num = 0;
        for step in self.steps:
            num += 1
            type = step['type']
            if (type == 'mix'):
                if (t < mix_time):
                    t = mix_time
            elif (type == 'infuse'):
                water += step['volume']
            # Current state
            # FIXME - following assumes all grains present in recipe
            vol = water_grain_volume( water, self.total_grains() )  
            if (num>1):
                stage.append({'type': type, 'time': t, 'volume': vol, 
                              'water': water, 'temp': temp})
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
                decoction_water = water * step['frac']
                water = water - decoction_water
                print("deco water: %s" % decoction_water)
                step['decoction'].ingredient('water','decoction',decoction_water)
                step['decoction'].find_stages(stages, decoction_name, t)
            elif (type == 'mix'):
                water += step['decoction'].total_water()
                print("mixing: %s %s %s" % (mash_name, str(t),str(step['decoction'].total_water())))
        # add final state
        stage.append({'type': 'end_state', 'time': t, 'volume': vol, 
                      'water': water, 'temp': temp})
        # no return val, data left in stage 

    def total_time(self):
        """Return the total time that this mash takes to complete.
 
        Does not deal with decoctions but is useful to calculate the time
        of a decoction which is part of a main mash.
        """
        t = timedelta()
        for step in self.steps:
            if ('time' in step):
                t += self.parsetime(step['time']) 
        return(t)
      
