"""Implement Step Mash as specialization of Mash."""
from .mash import Mash
from .quantity import Quantity

from datetime import timedelta


class StepMash(Mash):
    """A step mash where ingredients may be added and temperatures changed.

    Each step in the mash is recorded as a sub-recipe but, unlike the normal
    case of sub-recipes, the steps are not full recipe objects but a simpler
    description (a dict) of the part of the mash process.
    """

    DEFAULT_NAME = 'step mash'

    def __init__(self, **kwargs):
        """Initialize StepMash, pass arguments to Mash superclass."""
        super(StepMash, self).__init__(**kwargs)

    def add_step(self, type, **extra):
        """Add step to the mash process.

        In most cases we are doing the same sorts of things as an infusion
        mash, such as heating, waiting, etc. However, the key distinguishing
        parts are the abilities to split and to mix mashes (ie. take and
        recombine decoctions).
        """
        extra['type'] = type
        # Make quantities from time, volume, temp
        if ('time' not in extra):
            extra['time'] = Quantity('0min')
        else:
            extra['time'] = Quantity(extra['time'])
        if ('volume' in extra):
            extra['volume'] = Quantity(extra['volume'])
        if ('temp' in extra):
            extra['temp'] = Quantity(extra['temp'])
        # Known types
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
            raise Exception('Unknown step type "%s"' % (type))

    def total_water(self):
        """Add up all water to return total volume.

        Go through all the step of this mash adding up all water
        additions. Also add water ingredients and any from a
        preceding mash.
        """
        total_water = self.total_type('water', 'gal')  # ingredients
        if (self.import_property('total_water', 'start_water')):
            total_water += self.property('start_water')
        for step in self.steps:
            if ('type' in step and step['type'] == 'infuse' and
                    'volume' in step):
                total_water += step['volume']
        return(total_water)

    def total_time(self):
        """Return the total time that this mash takes to complete.

        This is just the sum of the times of the individual steps
        in the mash.
        """
        t = timedelta()
        for step in self.steps:
            if ('time' in step):
                t += self.parsetime(step['time'])
        return(t)

    def steps_str(self, start_time=timedelta(), n=0, indent=''):
        """Write out a time sequence of all steps, including decoctions.

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
        stages_iter = {}
        stages_next = {}
        stages_started = {}
        s = "H:MM:SS "
        for mash in mashes:
            s += "| %-27s " % (mash)
            stages_iter[mash] = iter(stages[mash])
            stages_next[mash] = next(stages_iter[mash])
            stages_started[mash] = 0
        s += '\n'
        # Keep looking at all lists of stages to find next time, exit when all done
        while True:
            # Find lowest time in nexts
            t = timedelta(days=9999)  # big
            for mash in mashes:
                if (stages_next[mash] and stages_next[mash]['time'] < t):
                    t = stages_next[mash]['time']
            # Output all things that happen at time t
            s += str(t) + ' '
            for mash in mashes:
                state = ''
                if (stages_next[mash]):
                    if (stages_next[mash]['time'] <= t):
                        state = self.stage_state_str(stages_next[mash])
                        stages_started[mash] += 1
                        try:
                            stages_next[mash] = next(stages_iter[mash])
                        except StopIteration:
                            stages_next[mash] = None
                    elif (stages_started[mash] > 0):
                        state = '    -ditto-'
                    else:
                        state = ''  # '-not-started-'
                else:
                    state = ''  # '-end-'
                s += "| %-27s " % (state)
            s += '\n'
            # Are we done? All iterators used up
            not_none = 0
            for mash in mashes:
                if (stages_next[mash]):
                    not_none += 1
            if (not_none == 0):
                break
        return s

    def stage_state_str(self, stage):
        """Return string describing this stage."""
        str = "%s -> %s @ %s " % (stage['type'], stage['volume'], stage['temp'])
        return str

    def find_stages(self, stages, mash_name='_main', start_time=timedelta()):
        """Create list for this mash's stages in main stages dict."""
        stage = []
        stages[mash_name] = stage
        #
        t = start_time
        vol = Quantity('0gal')
        temp = Quantity()
        num = 0
        for step in self.steps:
            num += 1
            type = step['type']
            # Current state
            if (num > 1):
                stage.append({'type': step['type'], 'time': t, 'volume': vol, 'temp': temp})
            if ('volume' in step):
                vol = step['volume']
            if ('temp' in step):
                temp = step['temp']
            # Action of this step
            action = {}
            action.update(step)
            action['time'] = t
            if ('time' in step):
                t += self.parsetime(step['time'])
        # add final state
        stage.append({'type': 'state', 'time': t, 'volume': vol, 'temp': temp})
        # no return val, data left in stage

    def parsetime(self, tstr):
        """Parse time."""
        tqty = Quantity(tstr).to('min')
        return timedelta(minutes=tqty)

    def __str__(self, **kwargs):
        """String representation without steps."""
        # Use superclass str() but don't try to render steps
        s = super(StepMash, self).__str__(skip_steps=1)
        if 'skip_steps' not in kwargs:
            # Now render the steps in our own special way
            s += '***steps***\n'
            s += self.steps_str()
        return s
